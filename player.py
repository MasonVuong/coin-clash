import pygame as pg; pg.init()
import math
from coin import Coin

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 3
        self.float_x = 100
        self.float_y = 50
        self.surface = pg.image.load("assets/pig.png").convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.float_x, self.float_y)
        self.coins = []
        self.shoot_cooldown = .25
        self.shoot_timer = 1
        self.range = 200

    def draw(self, window):
        for coin in self.coins:
                    coin.draw(window)
        window.blit(self.surface, self.rect)

    def update(self, seconds):
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

        self.shoot_timer += seconds

        center_x = self.rect.x + self.rect.width / 2
        center_y = self.rect.y + self.rect.height / 2
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            if keys[pg.K_i]:
                self.coins.append(Coin(1, center_x, center_y, center_x, center_y - self.range))
            elif keys[pg.K_j]:
                self.coins.append(Coin(1, center_x, center_y, center_x - self.range, center_y))
            elif keys[pg.K_k]:
                self.coins.append(Coin(1, center_x, center_y, center_x, center_y + self.range))
            elif keys[pg.K_l]:
                self.coins.append(Coin(1, center_x, center_y, center_x + self.range, center_y))
            else:
                self.shoot_timer = self.shoot_cooldown
            

        to_remove = []
        for coin in self.coins:
            if coin.update():
                to_remove.append(coin)
        for coin in to_remove:
            self.coins.remove(coin)  

        