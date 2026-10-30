import pygame as pg; pg.init()
import math, random
from coin import Coin
from helper import Helper

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 3
        self.float_x = x
        self.float_y = y
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

        self.nickel_chance = 0
        self.dime_chance = 0
        self.quarter_chance = 0
        self.silver_dollar_chance = 0
        self.money = 31
        self.boss = None

        self.font = pg.font.Font(None, 25)

        self.rest = False

    def draw(self, window):
        if self.health > 0:
            self.draw_ui(window)
            for coin in self.coins:
                coin.draw(window)
            window.blit(self.surface, self.rect)

    def update(self, seconds):
        if self.rest:
            return
        if self.health <= 0:
            return "died"
        
        self.invincible -= seconds
        if self.invincible < 0:
            self.invincible = 0
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
                self.coins.append(Coin(coin_type, self.rect.centerx, self.rect.centery, self.rect.centerx + self.range * direct_x * diagonal, self.rect.centery + self.range * direct_y * diagonal))
            
        to_remove = []
        for coin in self.coins:
            if coin.check_collision(self.boss.rect):
                to_remove.append(coin)
                rewards = self.boss.damage(coin)
                if rewards[0]:
                    for coin in to_remove:
                        self.coins.remove(coin)  
                    return rewards[1]
            elif coin.update():
                to_remove.append(coin)
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
    def damage(self, amount):
        if self.invincible == 0:
            self.health -= amount
            self.invincible = self.damage_buffer_time
            return True
        return False
    def set_boss(self, boss):
        self.boss = boss
    def draw_ui(self, window):
        if int(self.invincible * 5) % 2 == 0:
            for i in range(self.health):
                window.blit(self.heart, pg.Rect(1 + i * 15, 1, 13, 13))
        text = "$" + str(self.money / 100)
        if self.money % 10 == 0:
            text += "0"
        text_surface = self.font.render(text, False, (0, 0, 0))
        window.blit(text_surface, (self.health * 15 + 15, 1))

    def reset(self, x, y):
        self.rest = False
        self.float_x = x
        self.float_y = y
        self.rect.x = self.float_x
        self.rect.y = self.float_y
        

        