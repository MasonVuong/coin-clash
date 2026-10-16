import pygame as pg; pg.init()
import math, random
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
            direct_x = 0
            direct_y = 0
            if keys[pg.K_i]:
                direct_y -= 1
            if keys[pg.K_j]:
                direct_x -= 1
            if keys[pg.K_k]:
                direct_y += 1
            if keys[pg.K_l]:
                direct_x += 1
            if (direct_x != 0 or direct_y != 0):
                self.shoot_timer = 0
                if (direct_x != 0 and direct_y != 0):
                    diagonal = 2 ** .5
                else:
                    diagonal = 1
                self.coins.append(Coin(random.choice([1, 5, 10, 25, 100]), self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2, self.rect.x + self.rect.width / 2 + self.range * direct_x * diagonal, self.rect.y + self.rect.height / 2 + self.range * direct_y * diagonal))
            

        to_remove = []
        for coin in self.coins:
            if coin.update():
                to_remove.append(coin)
        for coin in to_remove:
            self.coins.remove(coin)  

        