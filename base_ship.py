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
        self.current_health = 20
        self.target_health = 40
        self.max_health = 100
        self.health_bar_length = 50 # Size of ships
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = .5
        self.health_bar_offset = self.HEIGHT + 15

    # Create function get_damage() to handle damage for all classes

    # Create function get_health() to handle damage for all classes

    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0,255,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio) * -1
            transition_color = (255,255,0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar_rect = pygame.Rect(self.x, self.y + self.health_bar_offset, health_bar_width, HEALTH_BAR_HEIGHT)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, self.y + self.health_bar_offset, transition_width, HEALTH_BAR_HEIGHT)

        pygame.draw.rect(self.WIN, (255,0,0), health_bar_rect)
        pygame.draw.rect(self.WIN, transition_color, transition_bar_rect)
        pygame.draw.rect(self.WIN, (255,255,255), (self.x, self.y + self.health_bar_offset, self.health_bar_length, HEALTH_BAR_HEIGHT), 1)

    def update_location(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.x = x
        self.hitbox.y = y