import pygame as pg; pg.init()
from dollar_bill import DollarBill

class Coin(pg.sprite.Sprite):
    speed = 5
    def __init__(self, value, x, y, target_x, target_y):
        super().__init__()
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        diff_x = target_x - x
        diff_y = target_y - y
        distance = (diff_x ** 2 + diff_y ** 2) ** .5
        self.speed_x = diff_x * Coin.speed / distance
        self.speed_y = diff_y * Coin.speed / distance

    def draw(self, screen):
        pg.draw.circle(screen, (0, 0, 0), (self.x, self.y), 10)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        diff_x = self.target_x - self.x
        diff_y = self.target_y - self.y
        distance = (diff_x ** 2 + diff_y ** 2) ** .5
        if distance <= Coin.speed:
            return True
        return False
