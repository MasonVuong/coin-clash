import pygame as pg; pg.init()
import sys, os

from player import Player
from dollar_bill import DollarBill
from helper import Helper

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

player_start_x = 50
player_start_y = 100
boss_start_x = 200
boss_start_y = 25

player = Player(player_start_x, player_start_y)
boss = DollarBill(player, boss_start_x, boss_start_y)
player.rest = True
boss.rest = True
player.set_boss(boss)
floor_coins = []

background_surface = pg.image.load(Helper.resource_path("assets/boxing_ring.png")).convert_alpha()
background_rect = background_surface.get_rect()

shop_offset = 320 / 5

damage_icon_surface = pg.image.load(Helper.resource_path("assets/damage_icon.png")).convert_alpha()
damage_icon_rect = damage_icon_surface.get_rect()
damage_icon_rect.centerx = shop_offset
damage_icon_rect.centery = 90

coin_luck_surface = pg.image.load(Helper.resource_path("assets/coin_luck_icon.png")).convert_alpha()
coin_luck_rect = coin_luck_surface.get_rect()
coin_luck_rect.centerx = 2 * shop_offset
coin_luck_rect.centery = 90

speed_surface = pg.image.load(Helper.resource_path("assets/speed_icon.png")).convert_alpha()
speed_rect = speed_surface.get_rect()
speed_rect.centerx = 3 * shop_offset
speed_rect.centery = 90

health_surface = pg.image.load(Helper.resource_path("assets/health_icon.png")).convert_alpha()
health_rect = health_surface.get_rect()
health_rect.centerx = 4 * shop_offset
health_rect.centery = 90

run = True
debug = False
cheats = False
player_points = 0
boss_points = 0
last_winner = None

blue = (6, 90, 181)
red = (255, 0, 7)
big_font = pg.font.Font(None, 35)
small_font = pg.font.Font(None, 20)
state = "title"

pg.mouse.set_visible(False)

while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                run = False
            if e.key == pg.K_SPACE:
                if state == "title":
                    boss.rest = False
                    player.rest = False
                    state = "fight"
                elif debug and state == "fight":
                    if cheats:
                        player.damage_multiplier -= 100
                        cheats = False
                    else:
                        player.damage_multiplier += 100
                        cheats = True
                elif state == "message":
                    if player.health > 0:
                        message_timer = 0
                        state = "shop"
                    else:
                        state = "title"
                        player = Player(player_start_x, player_start_y)
                        boss = DollarBill(player, boss_start_x, boss_start_y)
                        player.rest = True
                        boss.rest = True
                        player.set_boss(boss)
                        floor_coins = []
                        player_points = 0
                        boss_points = 0
                        last_winner = None
                elif state == "shop":
                    player.reset(player_start_x, player_start_y)
                    boss.reset(boss_start_x, boss_start_y)
                    state = "fight"
            if state == "shop":
                if e.key == pg.K_i and player.money >= 10:
                    player.damage_multiplier += 0.1
                    player.money -= 10
                if e.key == pg.K_j and player.money >= 10:
                    player.upgrade_coin_luck()
                    player.money -= 10
                if e.key == pg.K_k and player.money >= 10:
                    player.speed += .1
                    player.money -= 10
                if e.key == pg.K_l and player.money >= 10:
                    player.health += 1
                    player.money -= 10

    seconds = clock.tick(60) / 1000.0

    rewards = player.update(seconds)
    if rewards == "died":
        boss_points += 1
        last_winner = "boss"
        boss.rest = True
        player.rest = True
        state = "message"

    elif rewards != None:
        for coin in rewards:
            floor_coins.append(coin)
        
    if boss.update(seconds) == "died":
        player_points += 1
        last_winner = "player"
        player.rest = True
        boss.rest = True
        state = "message"

    
    canvas.blit(background_surface, background_rect)
    if state == "message":
        pg.draw.ellipse(canvas, blue if last_winner == "player" else red, pg.Rect(70, 45, 180, 90))
        text = "Piggy Won!" if last_winner == "player" else "Game Over"
        text_surface = big_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (160 - text_surface.width / 2, 90 - text_surface.height / 2))
        text = "Space to Continue"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (160 - text_surface.width / 2, 90 - text_surface.height / 2 + 30))

    elif state == "shop":
        pg.draw.ellipse(canvas, (255, 241, 232), pg.Rect(20, 30, 280, 120))
        canvas.blit(damage_icon_surface, damage_icon_rect)
        canvas.blit(coin_luck_surface, coin_luck_rect)
        canvas.blit(health_surface, health_rect)
        canvas.blit(speed_surface, speed_rect)
        text = "I: 10¢"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (shop_offset - text_surface.width / 2, 90 - text_surface.height / 2 + 30))
        text = "J: 10¢"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (2 * shop_offset - text_surface.width / 2, 90 - text_surface.height / 2 + 30))
        text = "K: 10¢"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (3 * shop_offset - text_surface.width / 2, 90 - text_surface.height / 2 + 30))
        text = "L: 10¢"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (4 * shop_offset - text_surface.width / 2, 90 - text_surface.height / 2 + 30))
    
        text = "Space to Continue"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (160 - text_surface.width / 2, 90 - text_surface.height / 2 + 50))
    
    elif state == "title":
        text = "Coin Clash"
        text_surface = big_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (160 - text_surface.width / 2, 90 - text_surface.height / 2 ))
        text = "Space to Continue"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (160 - text_surface.width / 2, 90 - text_surface.height / 2 + 20))
        text = "WASD to Move"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (160 - text_surface.width / 2, 90 - text_surface.height / 2 + 40))
        text = "IJKL to Shoot"
        text_surface = small_font.render(text, False, (0, 0, 0))
        canvas.blit(text_surface, (160 - text_surface.width / 2, 90 - text_surface.height / 2 + 60))

    if state != "message" or last_winner != "boss":
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