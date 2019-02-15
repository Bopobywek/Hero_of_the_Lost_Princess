import os
from random import choice
from time import sleep

import pygame
import pyganim

from player import Hero
from camera import Camera
from platform import draw_level, LevelPlatform
from sounds import Sounds
from button import Button
from background import Background
from boss import Troll
from cursor import Cursor


TITLE = "Hero of the Lost Princess"


class Game(object):

    def __init__(self, w, h):
        pygame.init()
        self.size = w, h
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(TITLE)
        pygame.display.flip()
        self.hero_is_died = pygame.sprite.Sprite()
        self.hero_is_died.image = pygame.image.load("data/hero_died.png")
        self.hero_is_died.rect = self.hero_is_died.image.get_rect()
        self.hero_is_win = pygame.sprite.Sprite()
        self.hero_is_win.image = pygame.image.load("data/win.png")
        self.hero_is_win.rect = self.hero_is_died.image.get_rect()
        self.dead = pygame.sprite.Group()
        self.win_sp = pygame.sprite.Group()
        self.hero_is_win.add(self.win_sp)
        self.hero_is_died.add(self.dead)
        self.camera = Camera(w, h)
        self.win_m, self.dead_m = False, False
        self.music = [pygame.mixer.Sound("data/background_music_1.ogg"),
                      pygame.mixer.Sound("data/background_music_2.ogg"),
                      pygame.mixer.Sound("data/background_music_3.ogg")]
        self.menu_music = pygame.mixer.Sound("data/music/main_menu.ogg")
        self.victory_music, self.dead_music = pygame.mixer.Sound("data/Victory.wav"), \
                                              pygame.mixer.Sound("data/dead.wav")
        self.menu_music.play(-1)
        self.hero_sprite = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
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
                                   208, 93, "bookFlip2.ogg", "new_game")
        self.hero = Hero(self.hero_sprite, 60, 60, Sounds().return_dict_of_sounds())
        self.hero.add(self.all_sprites)
        self.cursor_group = pygame.sprite.Group()
        self.cursor = Cursor(self.cursor_group)
        self.main_menu = True
        self.bg = Background(self.background_sprite)
        self.main_img = pygame.image.load("data/main_menu.png")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.fps = 40
        self.just_music = None
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.buttons.update(event)
                    for sprite in self.buttons:
                        if sprite.state():
                            if sprite.button_name == "new_game":
                                self.main_menu = False
                                draw_level(self.level_names[0], 46, 46,
                                           [self.platform_sprites, self.all_sprites, self.hero_sprite,
                                            self.princess_sprite, self.info_sprites, self.boss_sprite, self.enemy_sprites])
                                self.camera.update(self.hero)
                                sprite.pressed = False
                                self.menu_music.stop()
                                self.just_music = choice(self.music)
                                self.just_music.play(-1)
                                break
                if event.type == pygame.KEYDOWN:
                    if event.key == 32:
                        draw_level(self.level_names[0], 46, 46,
                                   [self.platform_sprites, self.all_sprites, self.hero_sprite,
                                    self.princess_sprite, self.info_sprites, self.boss_sprite, self.enemy_sprites])
                        self.camera.update(self.hero)
                        self.main_menu = False
                        self.menu_music.stop()
                        self.just_music = choice(self.music)
                        self.just_music.play(-1)
                if event.type == pygame.MOUSEMOTION:
                    self.buttons.update(event)
                    self.cursor.rect.x, self.cursor.rect.y = event.pos
        else:
            if not self.hero.dead and not self.hero.win:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.up_state = -1
                if pygame.key.get_pressed()[pygame.K_a]:
                    self.left_state = -1
                if pygame.key.get_pressed()[pygame.K_d]:
                    self.left_state = 1
                if pygame.key.get_pressed()[pygame.K_TAB]:
                    self.level_state = 1
                if pygame.key.get_pressed()[pygame.K_r]:
                    self.reload_level()
                    sleep(1)
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.reload()
                    sleep(1)
                if pygame.key.get_pressed()[pygame.K_f]:
                    self.attack = True
                self.update()
                self.left_state, self.up_state, self.attack = None, None, None
            elif self.hero.win:
                if not self.win_m:
                    self.just_music.stop()
                    self.victory_music.play(-1)
                    self.win_m = True
                self.win_sp.draw(self.screen)
                self.camera.update(self.hero_is_win)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.reload()
            else:
                if not self.dead_m:
                    self.just_music.stop()
                    self.dead_music.play(-1)
                    self.dead_m = True
                self.dead.draw(self.screen)
                self.camera.update(self.hero_is_died)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.reload()
        self.clock.tick(self.fps)
        pygame.display.flip()

    def reload(self):

        self.level_state = 0
        for el in self.platform_sprites:
            self.all_sprites.remove(el)
            self.platform_sprites.remove(el)
        for el in self.info_sprites:
            self.all_sprites.remove(el)
            self.info_sprites.remove(el)
        for sprite in self.princess_sprite:
            self.all_sprites.remove(self)
            self.princess_sprite.remove(sprite)
        for sprite in self.boss_sprite:
            self.all_sprites.remove(self)
            self.boss_sprite.remove(sprite)
        for sprite in self.enemy_sprites:
            self.all_sprites.remove(sprite)
            self.enemy_sprites.remove(sprite)
        self.hero.reload()
        self.main_menu = True
        self.just_music.stop()
        self.dead_music.stop()
        self.victory_music.stop()
        self.menu_music.play(-1)

    def reload_level(self):
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
        for sprite in self.enemy_sprites:
            self.all_sprites.remove(sprite)
            self.enemy_sprites.remove(sprite)
        self.hero.reload_level([self.platform_sprites, self.all_sprites, self.hero_sprite,
                                self.princess_sprite, self.info_sprites, self.boss_sprite, self.enemy_sprites],
                               self.level_names[self.level_state])

    def check_for_next_level(self):
        for sprite in self.platform_sprites:
            if pygame.sprite.collide_rect(self.hero, sprite) and isinstance(sprite, LevelPlatform):
                self.level_state = (self.level_state + 1) % len(self.level_names)
                return True
        return False

    def next_level(self):
        self.just_music.stop()
        self.just_music = choice(self.music)
        self.just_music.play(-1)
        self.reload_level()
        sleep(1)

    def update(self):
        for sprite in self.all_sprites:
            self.camera.apply(sprite)
        self.background_sprite.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.hero_sprite.update([self.platform_sprites, self.all_sprites, self.enemy_sprites, self.princess_sprite],
                                self.screen, self.left_state, self.up_state, self.attack)
        self.princess_sprite.update(self.platform_sprites)
        self.boss_sprite.update(self.platform_sprites, self.hero_sprite, self.screen)
        self.enemy_sprites.update(self.platform_sprites, self.hero_sprite, self.screen)
        self.platform_sprites.update(self.boss_sprite)
        self.camera.update(self.hero)
        if self.check_for_next_level():
            self.next_level()


if __name__ == '__main__':
    game = Game(800, 640)
    while game.running:
        game.draw()
