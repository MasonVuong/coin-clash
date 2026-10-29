import pygame as pg; pg.init()
from dollar_bill_state.dollar_bill_idle import DollarBillIdle
from coin import Coin

class DollarBillShoot:
    def __init__(self, boss):
        super().__init__()
        self.boss = boss
        self.wind_up_length = 0.7
        self.wind_up_timer = 0
        self.range = 150
        self.coin_iterate = 0
        self.coins = []
        self.x_direct = [-self.range, 0, 0, -self.range / (2 ** .5), -self.range / (2 ** .5)]
        self.y_direct = [0, self.range, -self.range, self.range / (2 ** .5), -self.range / (2 ** .5)]
    
    def update(self, seconds):
        self.wind_up_timer += seconds
        if self.coin_iterate < len(self.x_direct) * 2:
            hole = self.coin_iterate % 2
            i = int(self.coin_iterate / 2)
            self.coin_iterate += 1
            self.coins.append(Coin(Coin.random_coin_value(), self.boss.rect.x + 22 + 55 * hole, self.boss.rect.y + 22, self.boss.rect.x + 22 + 55 * hole + self.x_direct[i] * (-1 if hole == 1 else 1), self.boss.rect.y + 22 + self.y_direct[i]))
        if self.wind_up_timer >= self.wind_up_length:
            self.boss.state = DollarBillIdle(self.boss)
            return self.coins
        return None
    
    def draw(self, window):
        for x_off in range(2):
            for y_off in range(2):
                pg.draw.circle(window, (255, 0, 0), (self.boss.rect.x + 22 + x_off, self.boss.rect.y + 22 + y_off), self.wind_up_timer * 10)
                pg.draw.circle(window, (255, 0, 0), (self.boss.rect.x + 77 + x_off, self.boss.rect.y + 22 + y_off), self.wind_up_timer * 10)
