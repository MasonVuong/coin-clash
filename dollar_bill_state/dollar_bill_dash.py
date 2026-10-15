import pygame as pg; pg.init()
from dollar_bill_state.dollar_bill_idle import DollarBillIdle

class DollarBillDash(pg.sprite.Sprite):
    def __init__(self, boss, target_x, target_y):
        super().__init__()
        self.boss = boss
        self.target_x = target_x
        self.target_y = target_y
        diff_x = target_x - (self.boss.rect.x + self.boss.rect.width / 2)
        diff_y = target_y - (self.boss.rect.y + self.boss.rect.height / 2)
        distance = (diff_x ** 2 + diff_y ** 2) ** .5
        self.speed_x = diff_x * self.boss.speed / distance
        self.speed_y = diff_y * self.boss.speed / distance

    def update(self, seconds):
        self.boss.float_x += self.speed_x
        self.boss.float_y += self.speed_y
        self.boss.rect.topleft = (self.boss.float_x, self.boss.float_y)
        diff_x = self.target_x - (self.boss.rect.x + self.boss.rect.width / 2)
        diff_y = self.target_y - (self.boss.rect.y + self.boss.rect.height / 2)
        distance = (diff_x ** 2 + diff_y ** 2) ** .5
        if distance <= self.boss.speed:
            self.boss.rect.x = self.target_x - self.boss.rect.width / 2
            self.boss.rect.y = self.target_y - self.boss.rect.height / 2
            self.boss.state = DollarBillIdle(self.boss)