import os
from time import time

import pygame
import pyganim

from platform import *
from boss import Troll

GRAVITY = 0.3
SPEED = 10
JUMP = 10
HURT_TIMEOUT = 3

ANIMATION_RIGHT = [(pygame.transform.scale(pygame.image.load(os.path.join("data/png/walk", i)), (78, 96)),
                    pygame.time.Clock().tick(20))
                   for i in os.listdir("data/png/walk")]

ANIMATION_LEFT = [(pygame.transform.flip(pygame.transform.scale(pygame.image.load(
    os.path.join("data/png/walk", i)), (78, 96)), True, False), pygame.time.Clock().tick(20))
    for i in os.listdir("data/png/walk")]

ANIMATION_LEFT_ATTACK = [(pygame.transform.flip(pygame.transform.scale(pygame.image.load(
    os.path.join("data/png/attack", i)), (78, 96)), False, False), pygame.time.Clock().tick(10))
    for i in os.listdir("data/png/attack")]

ANIMATION_RIGHT_ATTACK = [(pygame.transform.flip(pygame.transform.scale(pygame.image.load(
    os.path.join("data/png/attack", i)), (78, 96)), True, False), pygame.time.Clock().tick(10))
    for i in os.listdir("data/png/attack")]

ANIMATION_JUMP = [(pygame.transform.scale(pygame.image.load(os.path.join("data/png/jump", i)), (78, 96)),
                   pygame.time.Clock().tick(10))
                  for i in os.listdir("data/png/jump")]

ANIMATION_STAY = [
    (pygame.transform.scale(pygame.image.load(os.path.join("data/png/idle", i)), (78, 96)), 100)
    for i in os.listdir("data/png/idle")]

ANIMATION_JUMP_LEFT = [(pygame.transform.flip(pygame.transform.scale(
    pygame.image.load(os.path.join("data/png/jump", i)), (78, 96)), True, False), pygame.time.Clock().tick(10))
    for i in os.listdir("data/png/jump")]


class Hero(pygame.sprite.Sprite):

    def __init__(self, group, x, y, sounds):
        super().__init__(group)
        self.sounds = sounds
        self.speed_x, self.speed_y = 0, 0
        self.rect = pygame.Rect(x, y, 50, 85)
        self.image = pygame.Surface((55, 85), pygame.SRCALPHA, 32)
        self.health = 100
        self.start_pos = (x, y)
        self.ground = False
        self.time_hurt = time()
        self.right_anim = pyganim.PygAnimation(ANIMATION_RIGHT)
        self.right_anim.play()
        self.left_anim = pyganim.PygAnimation(ANIMATION_LEFT)
        self.left_anim.play()
        self.stay_anim = pyganim.PygAnimation(ANIMATION_STAY)
        self.stay_anim.play()
        self.jump_anim = pyganim.PygAnimation(ANIMATION_JUMP)
        self.jump_anim.play()
        self.jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.jump_left.play()
        self.attack_anim = pyganim.PygAnimation(ANIMATION_RIGHT_ATTACK)
        self.attack_anim.play()
        self.attack_anim_2 = pyganim.PygAnimation(ANIMATION_LEFT_ATTACK)
        self.attack_anim_2.play()
        self.sounds["walk"].set_volume(0.3)
        self.sounds["jump"].set_volume(1.0)
        self.sounds_timeout = {i: time() for i in sounds}
        self.rect.x, self.rect.y = x, y
        self.last_turn = None
        self.attack = False

    def collide_boss(self, group):
        self.rect.width += 20
        for sprite in group:
            if pygame.sprite.collide_rect(sprite, self) and isinstance(sprite, Troll):
                if self.attack:
                    sprite.damage()
                if self.time_hurt is not None:
                    if round(time()) - round(self.time_hurt) > HURT_TIMEOUT and sprite.attack:
                        self.health -= 13
                        self.time_hurt = time()
                else:
                    self.time_hurt = time()
        self.rect.width -= 20

    def health_check(self):
        if self.health <= 0:
            self.kill()
            raise SystemExit

    def collision_y(self, sprites_group):
        for sprite in sprites_group:
            if pygame.sprite.collide_rect(sprite, self) and not isinstance(sprite, Sign):
                if self.speed_y > 0:
                    self.ground = True
                    self.speed_y = 0
                    self.rect.bottom = sprite.rect.top
                if self.speed_y < 0:
                    self.speed_y = 0
                    self.rect.top = sprite.rect.bottom

    def collision_x(self, sprites_group):
        for sprite in sprites_group:
            if pygame.sprite.collide_rect(sprite, self) and not isinstance(sprite, Sign):
                if self.speed_x > 0:
                    self.rect.right = sprite.rect.left
                if self.speed_x < 0:
                    self.rect.left = sprite.rect.right
                if isinstance(sprite, DestroyPlatform) and self.attack:
                    sprite.kill()

    def draw_health(self, surface, hp):
        pygame.draw.rect(surface, pygame.Color("red"), (0, 5, hp, 20))
        self.draw_text(surface, "Health {}%".format(round(self.health)))

    def update(self, group_collide, surface, left=None, up=None, attack=None):
        self.draw_health(surface, self.health)
        self.attack = attack
        if attack:
            if time() - self.sounds_timeout["hit"] >= 0.3:
                self.sounds["hit"].play()
                self.sounds_timeout["hit"] = time()
        if attack is not None and up is None and left is None and self.ground:
            self.rect.width += 10
            for sprite in group_collide[0]:
                if pygame.sprite.collide_rect(sprite, self):
                    if isinstance(sprite, DestroyPlatform):
                        sprite.kill()
            self.rect.width -= 10
            if self.last_turn == "left":
                self.attack_anim.blit(surface, (self.rect.x - 20, self.rect.y))
            else:
                self.attack_anim_2.blit(surface, (self.rect.x - 5, self.rect.y))
        if left is not None:
            self.sounds["walk"].stop()
            self.speed_x = left * SPEED
            if self.ground:
                self.sounds["walk"].play()
                if left > 0:
                    self.right_anim.blit(surface, (self.rect.x - 5, self.rect.y))
                else:
                    self.left_anim.blit(surface, (self.rect.x - 20, self.rect.y))
            else:
                if left > 0:
                    self.jump_anim.blit(surface, (self.rect.x - 5, self.rect.y))
                else:
                    self.jump_left.blit(surface, (self.rect.x - 20, self.rect.y))
            if left > 0:
                self.last_turn = "right"
            else:
                self.last_turn = "left"

        else:
            self.speed_x = 0
        if up is not None and self.ground:
            self.sounds["jump"].stop()
            self.sounds["jump"].play()
            self.ground = False
            self.speed_y = up * JUMP
        else:
            self.speed_y += GRAVITY

        if left is None and up is None and self.ground and not attack:
            self.sounds["jump"].stop()
            self.sounds["walk"].stop()
            self.stay_anim.blit(surface, (self.rect.x - 5, self.rect.y))
        if not self.ground:
            if self.speed_x > 0:
                self.jump_anim.blit(surface, (self.rect.x - 5, self.rect.y))
            elif self.speed_x < 0:
                self.jump_left.blit(surface, (self.rect.x - 20, self.rect.y))
            else:
                self.jump_anim.blit(surface, (self.rect.x - 5, self.rect.y))

        self.rect.y += self.speed_y
        self.collision_y(group_collide[0])

        self.rect.x += self.speed_x
        self.collision_x(group_collide[0])
        self.collide_boss(group_collide[1])
        self.health_check()

    def reload(self, all_sp, name_level):
        draw_level(name_level, 46, 46, all_sp)
        self.rect.x, self.rect.y = self.start_pos[0], self.start_pos[1]
        self.speed_x, self.speed_y = 0, 0

    def draw_text(self, surface, text):
        font = pygame.font.Font("CloisterBlack.ttf", 19)
        text = font.render(text, 1, pygame.Color("white"))
        text_x, text_y = 0, 2
        surface.blit(text, (text_x, text_y))
