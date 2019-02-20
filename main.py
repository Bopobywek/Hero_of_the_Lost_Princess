import os
from random import choice

import pygame
import pyganim

from player import Hero
from camera import Camera
from platform import draw_level
from sounds import Sounds
from button import Button
from background import Background


pygame.init()
size = width, height = 800, 640
screen = pygame.display.set_mode(size)
pygame.display.flip()

levels = ['intro.txt', '1.txt', '2.txt', 'final.txt']
menu_music = pygame.mixer.Sound("data/music/main_menu.ogg").play(-1)
background_music = ["data/background_music_1.ogg", "data/background_music_2.ogg", "data/background_music_3.ogg"]
back_m = pygame.mixer.Sound(choice(background_music))
camera = Camera(width, height)
hero_sprite = pygame.sprite.Group()
platform_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()
bg = pygame.sprite.Group()
princess = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()
new_game_btn = Button(buttons, "new_game_btn.png", "new_game_btn_2.png", 300, 127, "bookFlip2.ogg")
settings = Button(buttons, "settings_btn_2.png", "settings_btn.png", 300, 166, "bookFlip2.ogg")
draw_level("final", 46, 46, platform_sprites, all_sprites, enemy_group, boss_group, princess,
           coins_group, bricks_group)
hero = Hero(hero_sprite, 60, 60, Sounds().return_dict_of_sounds(), coins_group, enemy_group,
            boss_group, bricks_group)
hero.add(all_sprites)
cursor_group = pygame.sprite.Group()
cursor = pygame.sprite.Sprite()
cursor.image = pygame.image.load("data/cursor.png")
cursor.rect = cursor.image.get_rect()
cursor.add(cursor_group)
Background(bg)
main_menu = True
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
fps = 40
left_state, up_state, attack = None, None, None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if main_menu:
        screen.blit(pygame.image.load("data/main_menu.png"), (0, 0))
        buttons.draw(screen)
        cursor_group.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            buttons.update(event)
            for sprite in buttons:
                if sprite.state():
                    main_menu = False
                    menu_music.stop()
                    back_m.play(-1)
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    main_menu = False
                    menu_music.stop()
                    back_m.play(-1)
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.x, cursor.rect.y = event.pos
    else:
        bg.draw(screen)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            up_state = -1
        if pygame.key.get_pressed()[pygame.K_a]:
            left_state = -1
        if pygame.key.get_pressed()[pygame.K_d]:
            left_state = 1
        if pygame.key.get_pressed()[pygame.K_r]:
            hero.reload()
        if pygame.key.get_pressed()[pygame.K_f]:
            attack = True
        all_sprites.draw(screen)
        hero_sprite.update(platform_sprites, screen, left_state, up_state, attack)
        enemy_group.update(platform_sprites, hero_sprite, screen, attack)
        boss_group.update(platform_sprites, hero_sprite, screen)
        princess.update(platform_sprites, hero_sprite)
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)
        left_state, up_state, attack = None, None, None
    clock.tick(fps)
    pygame.display.flip()
