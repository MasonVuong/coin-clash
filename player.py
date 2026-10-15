import pygame as pg; pg.init()
import math

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dime_count = 3
        self.dime_angle = 0
        self.dime_distance = 30
        self.speed = 3
        self.dime_radius = 5
        self.spawn_cooldown = 3
        self.spawn_timer = 0
        self.float_x = 100
        self.float_y = 50
        self.surface = pg.image.load("assets/pig.png").convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.float_x, self.float_y)

    def draw(self, window):
        window.blit(self.surface, self.rect)

    def update(self, seconds):
        self.spawn_timer += seconds
        if self.spawn_timer >= self.spawn_cooldown:
            self.spawn_timer = 0
            self.dime_count += 1
        self.dime_angle += 3
        if self.dime_angle >= 360:
            self.dime_angle = 0
        keys = pg.key.get_pressed()

        diagonal = 1
        if (keys[pg.K_w] ^ keys[pg.K_s]) and (keys[pg.K_a] ^ keys[pg.K_d]):
            diagonal = 2 ** .5
        if keys[pg.K_w]:
            self.float_y -= self.speed / diagonal
        if keys[pg.K_a]:
            self.float_x -= self.speed / diagonal
        if keys[pg.K_s]:
            self.float_y += self.speed / diagonal
        if keys[pg.K_d]:
            self.float_x += self.speed / diagonal

        self.rect.topleft = (self.float_x, self.float_y)