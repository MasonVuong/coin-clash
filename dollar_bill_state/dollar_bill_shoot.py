import pygame as pg; pg.init()
from dollar_bill_state.dollar_bill_idle import DollarBillIdle

class DollarBillShoot:
    def __init__(self, boss):
            super().__init__()
            self.boss = boss
            self.wind_up_length = 0.7
            self.wind_up_timer = 0
    
    def update(self, seconds):
        self.wind_up_timer += seconds
        if self.wind_up_timer >= self.wind_up_length:
            self.boss.state = DollarBillIdle(self.boss)
            coins = []
            return coins
        return None
    def draw(self, window):
        for x_off in range(2):
            for y_off in range(2):
                pg.draw.circle(window, (255, 0, 0), (self.boss.rect.x + 22 + x_off, self.boss.rect.y + 22 + y_off), self.wind_up_timer * 10)
                pg.draw.circle(window, (255, 0, 0), (self.boss.rect.x + 77 + x_off, self.boss.rect.y + 22 + y_off), self.wind_up_timer * 10)
