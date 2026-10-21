import pygame as pg; pg.init()  
from dollar_bill_state.dollar_bill_idle import DollarBillIdle
from dollar_bill_state.dollar_bill_dash import DollarBillDash
from coin import Coin
import random

class DollarBill(pg.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.speed = 5
        self.state = DollarBillIdle(self)
        self.player = player
        self.float_x = 10
        self.float_y = 20
        self.surface = pg.image.load("assets/bill.png").convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.float_x, self.float_y)
        self.health = 250
        self.damage_done = 0
        self.coin_drop = 4
        self.time_alive = 0
        self.time_goal = 15
    def draw(self, window):
        if self.health > 0:
            window.blit(self.surface, self.rect)
    def update(self, seconds):
        if self.health > 0:
            self.state.update(seconds)
            self.time_alive += seconds
    def attack(self):
        if self.health > 0:
            self.state = DollarBillDash(self, self.player.rect.x + self.player.rect.width / 2, self.player.rect.y + self.player.rect.height / 2)
    def damage(self, coin):
        if self.health > 0:
            self.health -= coin.damage
            if self.health <= 0:
                print(self.time_alive)
                reward_coins = []
                for i in range(self.coin_drop + self.coin_drop - min(self.damage_done, self.coin_drop) + self.coin_drop * int(self.time_alive <= self.time_goal)):
                    reward_coins.append(Coin(Coin.random_coin_value(20, 10, 5, 1), self.rect.centerx + random.randint(-30, 30), self.rect.centery + random.randint(-30, 30), True))
                self.rect.x = -66743
                self.rect.y = -66743
                return (True, reward_coins)
        return (False, [])
    def check_collision(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False


    