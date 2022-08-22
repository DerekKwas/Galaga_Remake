import pygame

class Enemy:
    def __init__(self, x, y):
        WIDTH, HEIGHT = 50, 50

        self.health = 2
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(x, y, WIDTH, HEIGHT)

    def update_location(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.x = x
        self.hitbox.y = y