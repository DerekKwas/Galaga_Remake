from lib2to3.pytree import Base
from base_ship import Base_Ship
import random

class Enemy(Base_Ship):
    def __init__(self, x, y, health):
        super().__init__(x, y, health)
        print("NEW ENEMY CREATED!")
        self.health = 5
        self.canDamage = True
        self.DEFAULT_VEL = 2
        self.VELList = [(1,1), (0,1), (-1, 1)]
        self.VELOptions = [(1,1), (-1, 1)]
        self.VELIndex = 1
        self.currentVEL = (0,1)
        self.previousVEL = (-1,1)
        self.counter = 0
        self.COUNTER_MAX = 15

    def get_random_vel(self, WIN_WIDTH, WIN_HEIGHT):
        if self.counter >= self.COUNTER_MAX:
            self.counter = 0
            self.VELIndex = random.randint(0, len(self.VELOptions) -1)
            self.previousVEL = self.currentVEL
            self.VELOptions.append(self.previousVEL)
            self.currentVEL = self.VELOptions[self.VELIndex]
            del self.VELOptions[self.VELIndex]
        if self.y > WIN_HEIGHT:
            self.update_location(self.x, 0)
            self.canDamage = True
            self.counter += 1
        else:
            self.update_location(self.x + (self.currentVEL[0] * self.DEFAULT_VEL), self.y + (self.currentVEL[1] * self.DEFAULT_VEL))
            self.counter += 1
            # print(f"Current: {self.currentVEL}\nLast: {self.previousVEL}\nOptions: {self.VELOptions}")







        # ENEMY_VEL = self.VEL * random.choice((-1, 1))
        # if self.y > WIN_HEIGHT:
            # self.update_location(self.x, 0)
            # self.canDamage = True
        # else:
            # self.update_location(self.x, self.y + self.VEL)
        # self.update_location(self.x + ENEMY_VEL, self.y)