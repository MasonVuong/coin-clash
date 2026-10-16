import pygame as pg; pg.init()
from dollar_bill import DollarBill

class Coin(pg.sprite.Sprite):
    speed = 3
    def __init__(self, value, x, y, target_x, target_y):
        super().__init__()

        path = ""
        if value == 1:
            path = "assets/penny.png"
        elif value == 5:
            path = "assets/nickel.png"
        elif value == 10:
            path = "assets/dime.png"
        elif value == 25:
            path = "assets/quarter.png"
        elif value == 100:
            path = "assets/silver_dollar.png"
        self.surface = pg.image.load(path).convert_alpha()
        self.rect = self.surface.get_rect()

        self.rect.centerx = x
        self.rect.centery = y
        self.target_x = target_x
        self.target_y = target_y
        diff_x = target_x - x
        diff_y = target_y - y
        distance = (diff_x ** 2 + diff_y ** 2) ** .5
        self.speed_x = diff_x * Coin.speed / distance
        self.speed_y = diff_y * Coin.speed / distance

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        diff_x = self.target_x - self.rect.centerx
        diff_y = self.target_y - self.rect.centery
        distance = (diff_x ** 2 + diff_y ** 2) ** .5
        if distance <= Coin.speed:
            return True
        return False
