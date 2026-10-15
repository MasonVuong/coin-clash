import pygame as pg; pg.init()
import sys

from player import Player
from dollar_bill import DollarBill

VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 180

info = pg.display.Info()
MONITOR_WIDTH = info.current_w
MONITOR_HEIGHT = info.current_h

SCALE = min(MONITOR_WIDTH / VIRTUAL_WIDTH, MONITOR_HEIGHT / VIRTUAL_HEIGHT)
SCALE_WIDTH = int(VIRTUAL_WIDTH * SCALE)
SCALE_HEIGHT = int(VIRTUAL_HEIGHT * SCALE)

DESTINATION_X = (MONITOR_WIDTH - SCALE_WIDTH) // 2
DESTINATION_Y = (MONITOR_HEIGHT - SCALE_HEIGHT) // 2

window = pg.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT), pg.RESIZABLE)
canvas = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
clock = pg.time.Clock()

player = Player()
bill = DollarBill(player)

run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    seconds = clock.tick(60) / 1000.0

    player.update(seconds)
    bill.update(seconds)
    
    canvas.fill((255, 255, 255))
    bill.draw(canvas)
    player.draw(canvas)
    

    scaled_canvas = pg.transform.scale(canvas, (SCALE_WIDTH, SCALE_HEIGHT))
    window.blit(scaled_canvas, (DESTINATION_X, DESTINATION_Y))
    pg.display.flip()

pg.quit()
sys.exit()