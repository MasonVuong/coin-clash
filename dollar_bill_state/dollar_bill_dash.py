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
        diff_x = self.target_x - (self.boss.rect.x + self.boss.rect.width / 2)
        diff_y = self.target_y - (self.boss.rect.y + self.boss.rect.height / 2)
        distance = (diff_x ** 2 + diff_y ** 2) ** .5
        if distance <= self.boss.speed:
            self.boss.rect.x = self.target_x - self.boss.rect.width / 2
            self.boss.rect.y = self.target_y - self.boss.rect.height / 2
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
    