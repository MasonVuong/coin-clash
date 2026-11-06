import pygame as pg; pg.init()

class DollarBillIdle(pg.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.boss = boss
        self.attack_cooldown = 2
        self.attack_timer = 0
        self.animation_timer = 0
        self.animation_direction = 1

    def update(self, seconds):
        self.attack_timer += seconds
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            self.boss.attack()
        if self.boss.ground_slammed:
            self.animation_timer += seconds * self.animation_direction
    def draw(self, window):
        if not self.boss.ground_slammed:
            window.blit(self.boss.surface, self.boss.rect)
        else:
            animation_index = int(self.animation_timer * 40)
            if animation_index >= 5:
                self.animation_direction = -1
                window.blit(self.boss.ground_slammed_surfaces[4], self.boss.ground_slammed_rect)
            elif animation_index < 0:
                self.boss.ground_slammed = False
                window.blit(self.boss.surface, self.boss.rect)
            else:
                window.blit(self.boss.ground_slammed_surfaces[animation_index], self.boss.ground_slammed_rect)