import pygame as pg; pg.init()  
from dollar_bill_state.dollar_bill_idle import DollarBillIdle
from dollar_bill_state.dollar_bill_dash import DollarBillDash

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
    def draw(self, window):
        window.blit(self.surface, self.rect)
    def update(self, seconds):
        self.state.update(seconds)
    def attack(self):
        self.state = DollarBillDash(self, self.player.rect.x + self.player.rect.width / 2, self.player.rect.y + self.player.rect.height / 2)

    