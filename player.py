import pygame as pg; pg.init()
import math, random
from coin import Coin
from helper import Helper

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 3
        self.float_x = 150
        self.float_y = 50
        self.surface = pg.image.load(Helper.resource_path("assets/pig.png")).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.float_x, self.float_y)
        self.heart = pg.image.load(Helper.resource_path("assets/heart.png")).convert_alpha()
        self.coins = []
        self.shoot_cooldown = .25
        self.shoot_timer = 1
        self.range = 200
        self.health = 3
        self.invincible = 0
        self.damage_buffer_time = 3

        self.nickel_chance = 20
        self.dime_chance = 10
        self.quarter_chance = 5
        self.silver_dollar_chance = 1
        self.money = 0
        self.boss = None

        self.font = pg.font.Font(None, 30)

    def draw(self, window):
        self.draw_ui(window)
        for coin in self.coins:
            coin.draw(window)
        window.blit(self.surface, self.rect)

    def update(self, seconds):
        self.invincible -= seconds
        if self.invincible < 0:
            self.invincible = 0
        if self.check_collision(self.boss) and self.invincible == 0:
            self.health -= 1
            self.boss.damage_done += 1
            self.invincible = self.damage_buffer_time
        if self.health <= 0:
            return "died"
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
        if self.float_x < 0:
            self.float_x = 0
        if self.float_x > 320 - self.rect.width:
            self.float_x = 320 - self.rect.width
        if self.float_y < 0:
            self.float_y = 0
        if self.float_y > 180 - self.rect.height:
            self.float_y = 180 - self.rect.height
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
                coin_type = Coin.random_coin_value(self.nickel_chance, self.dime_chance, self.quarter_chance, self.silver_dollar_chance)
                self.coins.append(Coin(coin_type, self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2, self.rect.x + self.rect.width / 2 + self.range * direct_x * diagonal, self.rect.y + self.rect.height / 2 + self.range * direct_y * diagonal))
            

        to_remove = []
        for coin in self.coins:
            if coin.update():
                to_remove.append(coin)
            if coin.check_collision(self.boss.rect):
                to_remove.append(coin)
                rewards = self.boss.damage(coin)
                if rewards[0]:
                    for coin in to_remove:
                        self.coins.remove(coin)  
                    return rewards[1]
                

        for coin in to_remove:
            self.coins.remove(coin)  
        return None
    def pickup(self, object):
        if isinstance(object, Coin):
            self.money += object.value
    def check_collision(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False
    def set_boss(self, boss):
        self.boss = boss
    def draw_ui(self, window):
        if int(self.invincible * 5) % 2 == 0:
            for i in range(self.health):
                window.blit(self.heart, pg.Rect(10 + i * 22, 10, 18, 18))
        text = "$" + str(self.money / 100)
        if self.money % 10 == 0:
            text += "0"
        text_surface = self.font.render(text, False, (0, 0, 0))
        window.blit(text_surface, (10, 28))

        