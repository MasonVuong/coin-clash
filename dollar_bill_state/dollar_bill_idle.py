import pygame as pg; pg.init()

class DollarBillIdle(pg.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.boss = boss
        self.attack_cooldown = 2
        self.attack_timer = 0

    def update(self, seconds):
        self.attack_timer += seconds
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            self.boss.attack()