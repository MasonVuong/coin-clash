import pygame as pg; pg.init()
from dollar_bill_state.dollar_bill_idle import DollarBillIdle
from coin import Coin
import random
from helper import Helper

class DollarBillShoot:
    def __init__(self, boss, type=-1):
        super().__init__()
        self.boss = boss
        self.wind_up_timer = 0
        self.coin_iterate = 0
        self.coins = []
        if type == -1:
            type = random.choice(self.boss.shoot_attacks)
        self.type = type
        if type == "Around":
            self.wind_up_length = 0.7
            self.x_direct = [-self.boss.range, 0, 0, -self.boss.range / (2 ** .5), -self.boss.range / (2 ** .5)]
            self.y_direct = [0, self.boss.range, -self.boss.range, self.boss.range / (2 ** .5), -self.boss.range / (2 ** .5)]
        elif type == "3 Targeted":
            self.wind_up_length = 0.4
            diff_x = self.boss.player.rect.centerx - self.boss.rect.centerx
            diff_y = self.boss.player.rect.centery - self.boss.rect.centery
            theta, x_distance, y_distance = Helper.offset_targeting(diff_x, diff_y, self.boss.range, 20)
            theta2, x_distance2, y_distance2 = Helper.offset_targeting(diff_x, diff_y, self.boss.range, -20)
            self.x_direct = [self.boss.player.rect.centerx, self.boss.rect.centerx + x_distance, self.boss.rect.centerx + x_distance2]
            self.y_direct = [self.boss.player.rect.centery, self.boss.rect.centery + y_distance, self.boss.rect.centery + y_distance2]
    def update(self, seconds):
        self.wind_up_timer += seconds
        if self.type == "Around":
            if self.coin_iterate < len(self.x_direct) * 2:
                hole = self.coin_iterate % 2
                i = int(self.coin_iterate / 2)
                self.coin_iterate += 1
                self.coins.append(Coin(Coin.random_coin_value(self.boss.nickel_chance, self.boss.dime_chance, self.boss.quarter_chance, self.boss.silver_dollar_chance), self.boss.rect.x + 22 + 55 * hole, self.boss.rect.y + 22, self.boss.rect.x + 22 + 55 * hole + self.x_direct[i] * (-1 if hole == 1 else 1), self.boss.rect.y + 22 + self.y_direct[i]))
        if self.type == "3 Targeted":
            if self.coin_iterate < len(self.x_direct):
                self.coins.append(Coin(Coin.random_coin_value(self.boss.nickel_chance, self.boss.dime_chance, self.boss.quarter_chance, self.boss.silver_dollar_chance), self.boss.rect.centerx, self.boss.rect.centery, self.x_direct[self.coin_iterate], self.y_direct[self.coin_iterate]))
                self.coin_iterate += 1
        if self.wind_up_timer >= self.wind_up_length:
            self.boss.state = DollarBillIdle(self.boss)
            return self.coins
        return None
    
    def draw(self, window):
        if self.type == "Around":
            for x_off in range(2):
                for y_off in range(2):
                    pg.draw.circle(window, (255, 0, 0), (self.boss.rect.x + 22 + x_off, self.boss.rect.y + 22 + y_off), self.wind_up_timer * 10)
                    pg.draw.circle(window, (255, 0, 0), (self.boss.rect.x + 77 + x_off, self.boss.rect.y + 22 + y_off), self.wind_up_timer * 10)
        if self.type == "3 Targeted":
            pg.draw.circle(window, (255, 0, 0), (self.boss.rect.centerx, self.boss.rect.centery), self.wind_up_timer * 20)