import pygame as pg; pg.init()
import math

class Quarter(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 50
        self.dime_count = 10
        self.dime_angle = 0
        self.dime_distance = 50

    def draw(self, window):
        pg.draw.circle(window, (100, 100, 100), (self.x, self.y), 25)
        
        for i in range(self.dime_count): 
            dime_x = self.x + self.dime_distance * math.cos((self.dime_angle + i * 360 / self.dime_count) * math.pi / 180)
            dime_y = self.y + self.dime_distance * math.sin((self.dime_angle + i *360 / self.dime_count) * math.pi / 180)
            pg.draw.circle(window, (100, 100, 100), (dime_x, dime_y), 5)

    def update(self):
        self.dime_angle += 3
        if self.dime_angle >= 360:
            self.dime_angle = 0
        keys = pg.key.get_pressed()

        if (keys[pg.K_w]):
            self.y -= 1
        if (keys[pg.K_a]):
            self.x -= 1
        if (keys[pg.K_s]):
            self.y += 1
        if (keys[pg.K_d]):
            self.x += 1