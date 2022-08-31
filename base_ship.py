import pygame

# Constant Variable
HEALTH_BAR_HEIGHT = 10

class Base_Ship:
    def __init__(self, WIN, x, y):
        self.WIDTH, self.HEIGHT = 50, 50
        
        self.WIN = WIN
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    # Create function get_damage() to handle damage for all classes

    # Create function get_health() to handle damage for all classes

    def update_location(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.x = self.x
        self.hitbox.y = self.y