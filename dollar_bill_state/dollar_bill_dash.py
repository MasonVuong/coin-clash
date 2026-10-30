import pygame as pg; pg.init()
from dollar_bill_state.dollar_bill_idle import DollarBillIdle
from helper import Helper

class DollarBillDash(pg.sprite.Sprite):
    def __init__(self, boss, target_x, target_y):
        super().__init__()
        self.boss = boss
        self.target_x = target_x
        self.target_y = target_y
        distance, self.speed_x, self.speed_y = Helper.targeting(self.target_x, self.target_y, self.boss.rect.centerx, self.boss.rect.centery, self.boss.speed)
        self.wind_up_length = 0.7
        self.wind_up_timer = 0
        self.buffer_distance = 10

    def update(self, seconds):
        self.wind_up_timer += seconds
        if self.wind_up_timer >= self.wind_up_length:
            self.boss.float_x += self.speed_x
            self.boss.float_y += self.speed_y
        else:
            self.boss.float_x -= self.speed_x / 10
            self.boss.float_y -= self.speed_y / 10
        self.boss.rect.topleft = (self.boss.float_x, self.boss.float_y)
        distance = Helper.targeting(self.target_x, self.target_y, self.boss.rect.centerx, self.boss.rect.centery)
        if distance <= self.boss.speed:
            self.boss.rect.centerx = self.target_x
            self.boss.rect.centery = self.target_y
            self.boss.state = DollarBillIdle(self.boss)
        border = False
        if self.wind_up_timer >= self.wind_up_length:
            use_buffer = 1
        else:
            use_buffer = 0
        if self.boss.float_x < self.buffer_distance * use_buffer:
            if self.speed_x < 0 or self.wind_up_timer < self.wind_up_length:
                self.boss.float_x = self.buffer_distance * use_buffer
                border = True
        if self.boss.float_x > 320 - self.boss.rect.width - self.buffer_distance * use_buffer:
            if self.speed_x > 0 or self.wind_up_timer < self.wind_up_length:
                self.boss.float_x = 320 - self.boss.rect.width - self.buffer_distance * use_buffer
                border = True
        if self.boss.float_y < self.buffer_distance * use_buffer:
            if self.speed_y < 0 or self.wind_up_timer < self.wind_up_length:
                self.boss.float_y = self.buffer_distance * use_buffer
                border = True
        if self.boss.float_y > 180 - self.boss.rect.height - self.buffer_distance * use_buffer:
            if self.speed_y > 0 or self.wind_up_timer < self.wind_up_length:
                self.boss.float_y = 180 - self.boss.rect.height - self.buffer_distance * use_buffer
                border = True
        self.boss.rect.topleft = (self.boss.float_x, self.boss.float_y)
        if border and self.wind_up_timer >= self.wind_up_length:
            self.boss.state = DollarBillIdle(self.boss)
        elif border:
            self.wind_up_timer = self.wind_up_length

    def draw(self, window):
        pass
    