import pygame as pg; pg.init()
from dollar_bill_state.dollar_bill_idle import DollarBillIdle
from helper import Helper

class DollarBillSlam(pg.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.boss = boss
        self.air_timer = 0
        self.slam_cooldown = 2
        self.scale = 1
    def update(self, seconds):
        self.boss.rect.topleft = (self.boss.float_x, self.boss.float_y)
        if self.boss.shadow and self.air_timer < self.slam_cooldown:
            distance, self.speed_x, self.speed_y = Helper.targeting(self.boss.player.rect.centerx, self.boss.player.rect.centery, self.boss.rect.centerx, self.boss.rect.centery, self.boss.speed / 3)
            self.boss.float_x += self.speed_x
            self.boss.float_y += self.speed_y
            self.air_timer += seconds
    def draw(self, window):
        if not self.boss.shadow:
            if self.scale > 0:
                self.scale -= .02
                scaled_surface = pg.transform.scale(self.boss.surface, (self.boss.rect.width * self.scale, self.boss.rect.height * self.scale))
                scaled_rect = scaled_surface.get_rect()
                scaled_rect.centerx = self.boss.rect.centerx
                scaled_rect.centery = self.boss.rect.centery
                window.blit(scaled_surface, scaled_rect)
            else:
                self.boss.shadow = True
                self.scale = .25
        else:
            scaled_width = self.boss.rect.width * self.scale
            scaled_height = self.boss.rect.height * self.scale
            pg.draw.ellipse(window, (95, 87, 70), pg.Rect(self.boss.rect.centerx - scaled_width / 2, self.boss.rect.centery - scaled_height / 2, scaled_width, scaled_height))
            if self.air_timer >= self.slam_cooldown:
                self.scale += .04
            if self.scale >= 1:
                self.boss.state = DollarBillIdle(self.boss)
                self.boss.shadow = False