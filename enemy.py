from base_ship import Base_Ship
import os
import pygame
import random
import math
vec = pygame.math.Vector2

WIN_WIDTH = 600
WIN_HEIGHT = 600
MAX_WAYPOINTS = 2
DEFAULT_VEL = 0,0
MAX_SPEED = 4
MAX_FORCE = .1
APPROACH_RADIUS = 200

# Enemy images
ENEMY_LOW_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_Low.png"))
ENEMY_LOW = pygame.transform.rotate(ENEMY_LOW_IMAGE, 180)
ENEMY_MED_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_Med.png"))
ENEMY_MED = pygame.transform.rotate(ENEMY_MED_IMAGE, 180)
ENEMY_HIGH_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_High.png"))
ENEMY_HIGH = pygame.transform.rotate(ENEMY_HIGH_IMAGE, 180)

class Enemy(Base_Ship):
    def __init__(self, WIN, x, y):
        super().__init__(WIN, x, y)

        self.location = vec(x, y)
        self.velocity = vec(DEFAULT_VEL)
        self.acceleration = vec(0,0)

        self.waypoints = []
        self.generate_waypoints()
        self.targetIndex = 0
        self.target = self.waypoints[self.targetIndex]

        self.health = 3
        self.canDamage = True
        self.bullets = []
        
    def seek(self):
        # Steering force = desired velocity - current velocity
        self.desired_velocity = (self.target - self.location).normalize() * MAX_SPEED
        steer = (self.desired_velocity - self.velocity)
        steerLen = math.sqrt((math.pow(steer[0], 2)) + (math.pow(steer[1], 2)))

        if steerLen > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def update(self):
        self.desired_velocity = (self.target - self.location)
        dist = math.sqrt((math.pow(self.desired_velocity[0], 2)) + (math.pow(self.desired_velocity[1], 2)))                                   # len(self.desired_velocity)
        self.desired_velocity.normalize() * MAX_SPEED
        if dist < APPROACH_RADIUS:
            self.targetIndex += 1
            self.target = self.waypoints[self.targetIndex]
        else:
            self.target = self.waypoints[self.targetIndex]

        self.acc = self.seek()

        # Equations of motion
        self.velocity += self.acc
        if len(self.velocity) > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.location += self.velocity
        if self.location.x > WIN_WIDTH:
            self.location.x = 0
        if self.location.x < 0:
            self.location.x = WIN_WIDTH
        if self.location.y > WIN_HEIGHT:
            self.location.y = 0
            self.targetIndex = 0
            self.canDamage = True
        if self.location.y < 0:
            self.location.y = WIN_HEIGHT
        self.x = self.location.x
        self.y = self.location.y

    def generate_waypoints(self):
        while len(self.waypoints) < MAX_WAYPOINTS: # 2 will be max generated waypoints for now
            if len(self.waypoints) == 0:
                point = (random.randrange(0, WIN_WIDTH), WIN_HEIGHT/2)
                self.waypoints.append(point)
            else:
                point = (random.randrange(0, WIN_WIDTH), WIN_HEIGHT - self.HEIGHT)
                self.waypoints.append(point)
        point = (WIN_WIDTH/2, 1200)
        self.waypoints.append(point)

    def update_hitbox(self):
        self.hitbox.x = self.location.x
        self.hitbox.y = self.location.y

    def update_image(self):
        if self.health == 3:
            image = ENEMY_HIGH
        elif self.health == 2:
            image = ENEMY_MED
        else:
            image = ENEMY_LOW
        return image