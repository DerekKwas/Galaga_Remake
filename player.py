from base_ship import Base_Ship

class Player(Base_Ship):
    def __init__(self, WIN, x, y):
        super().__init__(WIN, x, y)
        self.health = 10