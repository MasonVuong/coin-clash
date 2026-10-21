import pygame as pg; pg.init()
import random

class Coin(pg.sprite.Sprite):
    speed = 4
    def __init__(self, value, x, y, target_x=-1, target_y=-1, pick_up=False):
        super().__init__()

        path = ""
        if value == 1:
            path = "assets/penny.png"
        elif value == 5:
            path = "assets/nickel.png"
        elif value == 10:
            path = "assets/dime.png"
        elif value == 25:
            path = "assets/quarter.png"
        elif value == 100:
            path = "assets/silver_dollar.png"
        self.surface = pg.image.load(path).convert_alpha()
        self.rect = self.surface.get_rect()

        self.rect.centerx = x
        self.rect.centery = y
        self.pick_up = pick_up
        self.value = value
        if not pick_up:
            self.target_x = target_x
            self.target_y = target_y
            diff_x = target_x - x
            diff_y = target_y - y
            distance = (diff_x ** 2 + diff_y ** 2) ** .5
            self.speed_x = diff_x * Coin.speed / distance
            self.speed_y = diff_y * Coin.speed / distance
            self.damage = value

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def update(self):
        if not self.pick_up:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            diff_x = self.target_x - self.rect.centerx
            diff_y = self.target_y - self.rect.centery
            distance = (diff_x ** 2 + diff_y ** 2) ** .5
            if distance <= Coin.speed:
                return True
        return False
        
    def check_collision(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False

    @staticmethod
    def random_coin_value(nickel, dime, quarter, silver):
        coin_roll = random.randint(0, 99)
        coin_type = 1
        if coin_roll in range(0, nickel):
            coin_type = 5
        elif coin_roll in range(nickel, nickel + dime):
            coin_type = 10
        elif coin_roll in range(nickel + dime, nickel + dime + quarter):
            coin_type = 25
        elif coin_roll in range(nickel + dime + quarter, nickel + dime + quarter + silver):
            coin_type = 100
        return coin_type
