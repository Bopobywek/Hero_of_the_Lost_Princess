import os

import pygame
import pyganim

from platform import *

GRAVITY = 0.4
SPEED = 10
JUMP = 10

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
    (pygame.transform.scale(pygame.image.load(os.path.join("data/png/idle", i)), (78, 96)), pygame.time.Clock().tick(5))
    for i in os.listdir("data/png/idle")]

ANIMATION_JUMP_LEFT = [(pygame.transform.flip(pygame.transform.scale(
    pygame.image.load(os.path.join("data/png/jump", i)), (78, 96)), True, False), pygame.time.Clock().tick(10))
    for i in os.listdir("data/png/jump")]


class Hero(pygame.sprite.Sprite):

    def __init__(self, group, x, y, sounds, sprite_group, monsters, boss_group, bricks):
        super().__init__(group)
        self.sounds = sounds
        self.speed_x, self.speed_y = 0, 0
        self.rect = pygame.Rect(x, y, 55, 90)
        self.image = pygame.Surface((55, 90), pygame.SRCALPHA, 32)
        self.start_pos = (x, y)
        self.ground = False
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
        self.rect.x, self.rect.y = x, y
        self.last_turn = None
        self.attack = False
        self.sprite_group = sprite_group
        self.health = 100
        self.monsters = monsters
        self.boss_group = boss_group
        self.coins = 0
        self.bricks = bricks

    def collision_y(self, sprites_group):
        for sprite in sprites_group:
            if pygame.sprite.collide_rect(sprite, self):
                if self.speed_y > 0:
                    self.ground = True
                    self.speed_y = 0
                    self.rect.bottom = sprite.rect.top
                if self.speed_y < 0:
                    self.speed_y = 0
                    self.rect.top = sprite.rect.bottom

    def collision_x(self, sprites_group):
        for sprite in sprites_group:
            if pygame.sprite.collide_rect(sprite, self):
                if self.speed_x > 0:
                    self.rect.right = sprite.rect.left
                if self.speed_x < 0:
                    self.rect.left = sprite.rect.right
                if isinstance(sprite, DestroyPlatform) and self.attack:
                    sprite.kill()

    def update(self, group, surface, left=None, up=None, attack=None):
        self.attack = attack
        if attack is not None and up is None and left is None and self.ground:
            # self.sounds["hit"].stop()
            # self.sounds["hit"].play()
            if self.last_turn == "left":
                self.attack_anim.blit(surface, (self.rect.x - 20, self.rect.y))
            else:
                self.attack_anim_2.blit(surface, (self.rect.x, self.rect.y))
        if left is not None:
            self.sounds["walk"].stop()
            self.speed_x = left * SPEED
            if self.ground:
                self.sounds["walk"].play()
                if left > 0:
                    self.right_anim.blit(surface, (self.rect.x, self.rect.y))
                else:
                    self.left_anim.blit(surface, (self.rect.x - 20, self.rect.y))
            else:
                if left > 0:
                    self.jump_anim.blit(surface, (self.rect.x, self.rect.y))
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
            self.stay_anim.blit(surface, (self.rect.x, self.rect.y))
        if not self.ground:
            if self.speed_x > 0:
                self.jump_anim.blit(surface, (self.rect.x, self.rect.y))
            elif self.speed_x < 0:
                self.jump_left.blit(surface, (self.rect.x - 20, self.rect.y))
            else:
                self.jump_anim.blit(surface, (self.rect.x, self.rect.y))

        if self.health <= 0:
            self.reload()

        self.health_f()

        self.draw_hp(surface)
        self.draw_coins(surface)
        self.collect_coins(self.sprite_group)
        self.kill(self.monsters)
        self.kill(self.boss_group)

        self.rect.y += self.speed_y
        self.collision_y(group)

        self.rect.x += self.speed_x
        self.collision_x(group)
        self.collision_x(self.bricks)

    def damage(self, n):
        self.health -= n

    def draw_coins(self, surface):
        self.draw_text(surface, "{}".format(self.coins), self.rect.x + 800//2 - 40,
                       self.rect.y - 640//2 + 80, 'yellow')

    def draw_hp(self, surface):
        pygame.draw.rect(surface, pygame.Color("red"), (self.rect.x,
                                                        self.rect.y - 20,
                                                        self.rect.width * (self.health / 100),
                                                        20))
        self.draw_text(surface, "{}%".format(round(self.health)),
                       self.rect.x, self.rect.y - 20, 'white')

    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font("14451.ttf", 19)
        text = font.render(text, 1, pygame.Color(color))
        text_x, text_y = x + self.rect.width // 2 - text.get_width() // 2, y
        surface.blit(text, (text_x, text_y))

    def collect_coins(self, sprite_group):
        for sprite in sprite_group:
            if pygame.sprite.collide_rect(self, sprite):
                self.coins += 1
                sprite.kill()

    def kill(self, monsters_group):
        for sprite in monsters_group:
            if pygame.sprite.collide_rect(self, sprite) and self.attack:
                sprite.damage()

    def health_f(self):
        if self.health < 50:
            self.health += 0.5

    def reload(self):
        self.rect.x, self.rect.y = self.start_pos[0], self.start_pos[1]
        self.speed_x, self.speed_y = 0, 0
