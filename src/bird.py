import pygame
import random
from constants import *

class Bird():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
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

    def jump(self):
        self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)
    
    def check_status(self, pipesList):
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipesList)

    def check_hits(self, pipesList):
        for pipe in pipesList:
            if pipe.rect.colliderect(self.rect):
                self.state = BIRD_DEAD
                break


    def update(self, dt, pipesList):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.draw()
            self.check_status(pipesList)
            
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
            if random.randint(0, 4) == 1:
                bird.jump()

            bird.update(dt, pipesList)

            if bird.state == BIRD_ALIVE:
                num_alive += 1
        
        return num_alive
    