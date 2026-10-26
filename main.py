import pygame as pg; pg.init()
import sys, os

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

player = Player(150, 50)
boss = DollarBill(player, 50, 50)
player.set_boss(boss)
floor_coins = []

run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    seconds = clock.tick(60) / 1000.0

    rewards = player.update(seconds)
    if rewards == "died":
        sys.exit()
    if rewards != None:
        for coin in rewards:
            floor_coins.append(coin)
        
    boss.update(seconds)
    
    canvas.fill((255, 255, 255))
    boss.draw(canvas)
    player.draw(canvas)
    to_remove = []
    for coin in floor_coins:
        coin.draw(canvas) 
        if coin.check_collision(player.rect):
            player.pickup(coin)
            to_remove.append(coin)
    for coin in to_remove:
        floor_coins.remove(coin)


    scaled_canvas = pg.transform.scale(canvas, (SCALE_WIDTH, SCALE_HEIGHT))
    window.blit(scaled_canvas, (DESTINATION_X, DESTINATION_Y))
    pg.display.flip()

pg.quit()
sys.exit()