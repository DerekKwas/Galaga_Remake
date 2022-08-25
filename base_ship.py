import pygame

class Base_Ship:
    def __init__(self, WIN, x, y, health):
        self.WIDTH, self.HEIGHT = 50, 50
        
        self.WIN = WIN
        self.x = x
        self.y = y
        self.health = health
        self.hitbox = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def update_location(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.x = x
        self.hitbox.y = y