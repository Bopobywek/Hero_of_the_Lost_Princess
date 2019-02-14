import os
from random import choice
from time import sleep

import pygame
import pyganim

from player import Hero
from camera import Camera
from platform import draw_level
from sounds import Sounds
from button import Button
from background import Background
from boss import Troll
from settings import Settings
from cursor import Cursor


class Game(object):

    def __init__(self, w, h):
        pygame.init()
        self.size = w, h
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.flip()
        self.hero_is_died = pygame.sprite.Sprite()
        self.hero_is_died.image = pygame.image.load("data/hero_died.png")
        self.hero_is_died.rect = self.hero_is_died.image.get_rect()
        self.dead = pygame.sprite.Group()
        self.hero_is_died.add(self.dead)
        self.camera = Camera(w, h)
        self.hero_sprite = pygame.sprite.Group()
        self.boss_sprite = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.princess_sprite = pygame.sprite.Group()
        self.info_sprites = pygame.sprite.Group()
        self.background_sprite = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.level_names = ["intro", "1", "2", "final"]
        self.level_state = 0
        self.new_game_btn = Button(self.buttons, "new_game_btn.png", "new_game_btn_2.png",
                                   300, 127, "bookFlip2.ogg", "new_game")
        self.settings = Button(self.buttons, "settings_btn_2.png", "settings_btn.png",
                               300, 166, "bookFlip2.ogg", "settings")
        self.hero = Hero(self.hero_sprite, 60, 60, Sounds().return_dict_of_sounds())
        self.hero.add(self.all_sprites)
        self.cursor_group = pygame.sprite.Group()
        self.cursor = Cursor(self.cursor_group)
        self.settings_menu = Settings(self.screen)
        self.settings_status = False
        self.main_menu = True
        self.bg = Background(self.background_sprite)
        self.main_img = pygame.image.load("data/main_menu.png")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.fps = 40
        self.left_state, self.up_state, self.attack = None, None, None
        self.running = True

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if self.main_menu:
            self.screen.blit(self.main_img, (0, 0))
            self.buttons.draw(self.screen)
            self.cursor_group.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.buttons.update(event)
                for sprite in self.buttons:
                    if sprite.state():
                        if sprite.button_name == "new_game":
                            self.main_menu = False
                            draw_level(self.level_names[0], 46, 46,
                                       [self.platform_sprites, self.all_sprites, self.hero_sprite,
                                        self.princess_sprite, self.info_sprites, self.boss_sprite])
                            self.camera.update(self.hero)
                            sprite.pressed = False
                            break
                        else:
                            self.main_menu = False
                            self.settings_status = True
                            sprite.pressed = False
                            break
                if event.type == pygame.KEYDOWN:
                    if event.key == 32:
                        self.main_menu = False
                if event.type == pygame.MOUSEMOTION:
                    self.cursor.rect.x, self.cursor.rect.y = event.pos
        else:
            if not self.hero.dead:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.up_state = -1
                if pygame.key.get_pressed()[pygame.K_a]:
                    self.left_state = -1
                if pygame.key.get_pressed()[pygame.K_d]:
                    self.left_state = 1
                if pygame.key.get_pressed()[pygame.K_TAB]:
                    self.level_state = 1
                if pygame.key.get_pressed()[pygame.K_r]:
                    self.reload()
                    sleep(1)
                if pygame.key.get_pressed()[pygame.K_f]:
                    self.attack = True
                self.update()
                self.left_state, self.up_state, self.attack = None, None, None
            else:
                self.dead.draw(self.screen)
                self.camera.update(self.hero_is_died)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.level_state = 0
                    for el in self.platform_sprites:
                        self.all_sprites.remove(el)
                        self.platform_sprites.remove(el)
                    for el in self.info_sprites:
                        self.info_sprites.remove(el)
                        self.all_sprites.remove(el)
                    for sprite in self.princess_sprite:
                        self.boss_sprite.remove(sprite)
                        self.all_sprites.remove(self)
                    for sprite in self.boss_sprite:
                        self.boss_sprite.remove(sprite)
                        self.all_sprites.remove(self)
                    self.hero.reload()
                    self.main_menu = True
        self.clock.tick(self.fps)
        pygame.display.flip()

    def reload(self):
        for el in self.platform_sprites:
            self.all_sprites.remove(el)
            self.platform_sprites.remove(el)
        for el in self.info_sprites:
            self.info_sprites.remove(el)
            self.all_sprites.remove(el)
        for sprite in self.princess_sprite:
            self.boss_sprite.remove(sprite)
            self.all_sprites.remove(self)
        for sprite in self.boss_sprite:
            self.boss_sprite.remove(sprite)
            self.all_sprites.remove(self)
        self.hero.reload_level([self.platform_sprites, self.all_sprites, self.hero_sprite,
                                self.princess_sprite, self.info_sprites, self.boss_sprite],
                               self.level_names[self.level_state])

    def update(self):
        for sprite in self.all_sprites:
            self.camera.apply(sprite)
        self.background_sprite.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.hero_sprite.update([self.platform_sprites, self.all_sprites],
                                self.screen, self.left_state, self.up_state, self.attack)
        self.princess_sprite.update(self.platform_sprites)
        self.boss_sprite.update(self.platform_sprites, self.hero_sprite, self.screen)
        self.camera.update(self.hero)


if __name__ == '__main__':
    game = Game(800, 640)
    while game.running:
        game.draw()
