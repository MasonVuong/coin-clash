import pygame as pg; pg.init()

class DollarBillIdle(pg.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.boss = boss
        self.attack_cooldown = 2
        self.attack_timer = 0
        self.animation_timer = 0

    def update(self, seconds):
        self.attack_timer += seconds
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            self.boss.attack()
        if self.boss.ground_slammed:
            self.animation_timer += seconds
    def draw(self, window):
        if not self.boss.ground_slammed:
            window.blit(self.boss.surface, self.boss.rect)
        else:
            animation_index = int(self.animation_timer * 20)
            if animation_index >= len(self.boss.ground_slammed_surfaces):
                window.blit(self.boss.surface, self.boss.rect)
            else:
                window.blit(self.boss.ground_slammed_surfaces[animation_index], self.boss.ground_slammed_rect)