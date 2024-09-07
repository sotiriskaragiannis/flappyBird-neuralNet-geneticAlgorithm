import random
import pygame
from constants import *

class Pipe():

    def __init__(self, gameDisplay, x, y, pipe_type):
        self.gameDisplay = gameDisplay
        self.pipe_type = pipe_type
        self.state = PIPE_MOVING
        self.img = pygame.image.load(PIPE_FILENAME)
        self.rect = self.img.get_rect() # Get rect reference
        if pipe_type == PIPE_UPPER:
            y = y - self.rect.height
        self.set_position(x, y)

    def set_position(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def move_position(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self):
        if self.rect.right < 0:
            self.state = PIPE_DONE

    def update(self, dt):
        if self.state == PIPE_MOVING:
            self.move_position(-PIPE_SPEED*dt, 0) # Negation because we want the pipe to move to the left
            self.draw()
            self.check_status()
            
class PipeCollection():
    
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.pipesList = []

    def add_new_pipe_pair(self, x):
        top_y = random.randint(PIPE_MIN, PIPE_MAX - PIPE_GAP_SIZE)
        bottom_y = top_y + PIPE_GAP_SIZE

        p1 = Pipe(self.gameDisplay, x, top_y, PIPE_UPPER)
        p2 = Pipe(self.gameDisplay, x, bottom_y, PIPE_LOWER)

        self.pipesList.append(p1)
        self.pipesList.append(p2)

    def create_new_set(self):
        self.pipesList = []
        placed = PIPE_FIRST
        
        # Add pipes until the placed pipe is off the screen
        while placed < DISPLAY_W + PIPE_START_X:
            self.add_new_pipe_pair(placed)
            placed += PIPE_ADD_GAP

    def update(self, dt):
        rightmost = 0
        for p in self.pipesList:
            p.update(dt)
            if p.rect.left > rightmost:
                rightmost = p.rect.left

        if rightmost < (DISPLAY_W - PIPE_ADD_GAP):
            self.add_new_pipe_pair(DISPLAY_W)
        
        # Remove pipes that are done
        self.pipesLIst = [p for p in self.pipesList if p.state == PIPE_MOVING]
