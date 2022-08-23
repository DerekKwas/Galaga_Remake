from pickle import NONE
import pygame

class Base_Ship:
    def __init__(self, x, y, health):
        self.WIDTH, self.HEIGHT = 50, 50
        
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def update_location(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.x = x
        self.hitbox.y = y