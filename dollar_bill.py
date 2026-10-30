import pygame as pg; pg.init()  
from dollar_bill_state.dollar_bill_idle import DollarBillIdle
from dollar_bill_state.dollar_bill_dash import DollarBillDash
from dollar_bill_state.dollar_bill_shoot import DollarBillShoot
from coin import Coin
import random
from helper import Helper

class DollarBill(pg.sprite.Sprite):
    def __init__(self, player, x, y):
        super().__init__()
        self.speed = 5
        self.state = DollarBillIdle(self)
        self.player = player
        self.float_x = x
        self.float_y = y
        self.surface = pg.image.load(Helper.resource_path("assets/bill.png")).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.float_x, self.float_y)
        self.health = 100
        self.max_health = 100
        self.range = 100
        self.damage_done = 0
        self.coin_drop = 4
        self.time_alive = 0
        self.time_goal = 15
        self.coins = []
        self.rest = False
        self.shoot_attacks = ["Around"]
        self.upgrade_level = 0

        self.nickel_chance = 0
        self.dime_chance = 0
        self.quarter_chance = 0
        self.silver_dollar_chance = 0
    def draw(self, window):
        if self.health > 0:
            window.blit(self.surface, self.rect)
            self.state.draw(window)
            for coin in self.coins:
                coin.draw(window)
    def update(self, seconds):
        if self.rest:
            return
        if self.health <= 0:
            return "died"
        
        if self.rect.colliderect(self.player.rect):
            if self.player.damage(1):
                self.damage_done += 1
        coins = self.state.update(seconds)
        if coins != None:
            for coin in coins:
                self.coins.append(coin)
        to_remove = []
        for coin in self.coins:
            if coin.check_collision(self.player.rect):
                if self.player.damage(1):
                    self.damage_done += 1
                to_remove.append(coin)
            elif coin.update():
                to_remove.append(coin)
        for coin in to_remove:
            self.coins.remove(coin)  
        self.time_alive += seconds
    def attack(self):
        if self.health > 0:
            distance = Helper.targeting(self.player.rect.centerx, self.player.rect.centery, self.rect.centerx, self.rect.centery)
            if distance < 75:
                self.state = DollarBillShoot(self)
            else:
                random_attack = random.randint(0, 1)
                if random_attack == 0:
                    self.state = DollarBillDash(self, self.player.rect.centerx, self.player.rect.centery)
                if random_attack == 1:
                    self.state = DollarBillShoot(self)
    def damage(self, coin):
        if self.health > 0:
            self.health -= coin.damage
            if self.health <= 0:
                reward_coins = []
                for i in range(self.coin_drop + self.coin_drop - min(self.damage_done, self.coin_drop) + self.coin_drop * int(self.time_alive <= self.time_goal)):
                    reward_coins.append(Coin(Coin.random_coin_value(20, 10, 5, 1), self.rect.centerx + random.randint(-30, 30), self.rect.centery + random.randint(-30, 30), pick_up=True))
                self.rect.x = -66743
                self.rect.y = -66743
                return (True, reward_coins)
        return (False, [])
    def check_collision(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False

    def reset(self, x, y):
        self.state = DollarBillIdle(self)
        self.rest = False
        self.float_x = x
        self.float_y = y
        self.rect.x = self.float_x
        self.rect.y = self.float_y
        self.upgrade_level += 1
        self.max_health *= 1.25
        self.health = self.max_health
        self.speed += 1
        self.range += 25
        if self.upgrade_level % 4 == 1:
            if self.upgrade_level == 1:
                self.dime_chance = 10
            else:
                self.dime_chance += 2
        elif self.upgrade_level % 4 == 2:
            if self.upgrade_level == 2:
                self.shoot_attacks.append("3 Targeted")
                self.nickel_chance = 20
            else:
                self.nickel_chance += 2
        elif self.upgrade_level == 3:
            if self.upgrade_level == 3:
                self.quarter_chance = 5
            else:
                self.quarter_chance += 2
        elif self.upgrade_level == 4:
            if self.upgrade_level == 4:
                self.silver_dollar_chance = 1
            else:
                self.silver_dollar_chance += 2

    