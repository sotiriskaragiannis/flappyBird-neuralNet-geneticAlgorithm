import pygame
import random
from constants import *
from neuralnet import NeuralNet
import numpy as np

class Bird():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.nn = NeuralNet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def reset(self):
        self.state = BIRD_ALIVE
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
    
    def move(self, dt):

        distance = 0
        new_speed = 0

        distance = self.speed * dt + 0.5 * GRAVITY * dt * dt # Calculate the distance the bird will move
        new_speed = self.speed + GRAVITY * dt # Calculate the new speed of the bird

        self.rect.centery += distance # Move the bird
        self.speed = new_speed  # Update the speed

        if self.rect.top < 0: # Check if the bird is above the screen 
            self.rect.top = 0
            self.speed = 0

    def jump(self, pipesList):
        inputs = self.get_inputs(pipesList)
        val = self.nn.get_max_value(inputs) # Get the output of the neural network
        # If the output is greater than the jump chance, jump
        if val > JUMP_CHANCE:
            self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)
    
    def check_status(self, pipesList):
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipesList)

    def assign_collision_fitness(self, pipe):
        gap_y = 0
        if pipe.pipe_type == PIPE_UPPER:
            gap_y = pipe.rect.bottom + PIPE_GAP_SIZE/2
        else:
            gap_y = pipe.rect.top - PIPE_GAP_SIZE/2
        
        self.fitness = -(abs(self.rect.centery - gap_y)) # Assign the fitness based on the distance from the gap

    def check_hits(self, pipesList):
        for pipe in pipesList:
            if pipe.rect.colliderect(self.rect):
                self.state = BIRD_DEAD
                self.assign_collision_fitness(pipe)
                break


    def update(self, dt, pipesList):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(pipesList)
            self.draw()
            self.check_status(pipesList)

    def get_inputs(self, pipesList):
        closest = DISPLAY_W * 2
        bottom_y = 0
        for pipe in pipesList:
            # Check if the pipe is an upper pipe and if it is closer than the current closest pipe
            if pipe.pipe_type == PIPE_UPPER and pipe.rect.right < closest and pipe.rect.right > self.rect.left:
                closest = pipe.rect.right # Update the closest pipe
                bottom_y = pipe.rect.bottom # Update the bottom y value of the pipe

        horizontal_distance = closest - self.rect.centerx # Calculate the horizontal distance between the bird and the closest pipe
        vertical_distance = self.rect.centery - (bottom_y + PIPE_GAP_SIZE/2) # Calculate the vertical distance between the bird and the closest pipe

        inputs = [
            ((horizontal_distance / DISPLAY_W) * 0.99) + 0.01,
            ((vertical_distance + Y_SHIFT) / NORMALIZER) * 0.99 + 0.01
        ]

        return inputs
    
    def create_offspring(p1, p2, gameDisplay):
        offspring = Bird(gameDisplay)
        offspring.nn.create_mixed_weights(p1.nn, p2.nn)
        return offspring
    
class BirdCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.birds = []
        self.create_new_generation()

    def create_new_generation(self):
        self.birds = []
        for i in range(GENERATION_SIZE):
            self.birds.append(Bird(self.gameDisplay))

    def update(self, dt, pipesList):
        num_alive = 0
        for bird in self.birds:
            bird.update(dt, pipesList)

            if bird.state == BIRD_ALIVE:
                num_alive += 1
        
        return num_alive
    
    def evolve_population(self):

            for b in self.birds:
                b.fitness += b.time_lived * PIPE_SPEED

            self.birds.sort(key=lambda x: x.fitness, reverse=True)

            cut_off = int(len(self.birds) * MUTATION_CUT_OFF)
            good_birds = self.birds[0:cut_off]
            bad_birds = self.birds[cut_off:]
            num_bad_to_take = int(len(self.birds) * MUTATION_BAD_TO_KEEP)

            for b in bad_birds:
                b.nn.modify_weights()

            new_birds = []

            idx_bad_to_take = np.random.choice(np.arange(len(bad_birds)), num_bad_to_take,  replace=False)

            for index in idx_bad_to_take:
                new_birds.append(bad_birds[index])

            new_birds.extend(good_birds)

            children_needed = len(self.birds) - len(new_birds)

            while len(new_birds) < len(self.birds):
                idx_to_breed = np.random.choice(np.arange(len(good_birds)), 2, replace=False)
                if idx_to_breed[0] != idx_to_breed[1]:
                    new_bird = Bird.create_offspring(good_birds[idx_to_breed[0]], good_birds    [idx_to_breed[1]], self.gameDisplay)
                    if random.random() < MUTATION_MODIFY_CHANCE_LIMIT:
                        new_bird.nn.modify_weights()
                    new_birds.append(new_bird)

            for b in new_birds:
                b.reset()

            self.birds = new_birds

