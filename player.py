from base_ship import Base_Ship

class Player(Base_Ship):
    def __init__(self, x, y, health):
        super().__init__(x, y, health)
        self.health = 10