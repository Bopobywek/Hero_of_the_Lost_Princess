import os
from time import time, sleep
from random import choice

import pygame
import pyganim

from sounds import Sounds

pygame.mixer.init()

ATTACK_TIMES = [5, 7, 10, 11]

ANIMATION_RIGHT = [(pygame.transform.scale(pygame.image.load(os.path.join("data/Troll2/walk", i)), (300, 320)),
                    150)
                   for i in os.listdir("data/Troll2/walk")] + [(pygame.transform.scale(
    pygame.image.load(os.path.join("data/Troll2/walk", i)), (300, 320)), 150)
                                                                    for i in os.listdir("data/Troll2/walk")][:-1:-1]

ANIMATION_LEFT = [(pygame.transform.flip(pygame.transform.scale(pygame.image.load(
    os.path.join("data/Troll2/walk", i)), (300, 320)), True, False), 150)
                     for i in os.listdir("data/Troll2/walk")] + [(pygame.transform.flip(pygame.transform.scale(
    pygame.image.load(os.path.join("data/Troll2/walk", i)), (300, 320)), True, False), 150)
                                                                    for i in os.listdir("data/Troll2/walk")][:-1:-1]

ANIMATION_STAY = [
    (pygame.transform.scale(pygame.image.load(os.path.join("data/Troll2/idle", i)), (300, 300)), 200)
    for i in os.listdir("data/Troll2/idle")] + [(pygame.transform.scale(
    pygame.image.load(os.path.join("data/Troll2/idle", i)), (300, 300)), 200)
                                                                    for i in os.listdir("data/Troll2/idle")][:-1:-1]

ANIMATION_JUMP = [
    (pygame.transform.scale(pygame.image.load(os.path.join("data/Troll2/jump", i)), (400, 520)), 100)
    for i in os.listdir("data/Troll2/jump")] + [(pygame.transform.scale(
    pygame.image.load(os.path.join("data/Troll2/jump", i)), (400, 520)), 100)
                                                                    for i in os.listdir("data/Troll2/jump")][:-1:-1]

GRAVITY = 0.5
SPEED = 5


class Troll(pygame.sprite.Sprite):

    def __init__(self, group, x, y):
        super().__init__(group)
        self.attack = False
        self.rect = pygame.Rect(x, y, 100, 200)
        self.image = pygame.Surface((100, 200), pygame.SRCALPHA, 32)
        self.rect.x, self.rect.y = x, y
        self.speed_y = 0
        self.speed_x = 0
        self.time_attack = choice(ATTACK_TIMES)
        self.stay_anim = pyganim.PygAnimation(ANIMATION_STAY)
        self.stay_anim.play()
        self.right_anim = pyganim.PygAnimation(ANIMATION_RIGHT)
        self.right_anim.play()
        self.sounds = Sounds().return_dict_of_sounds()
        self.health = 500
        self.last_hurt = time()
        self.anim_attack_time = time()
        self.attack = False
        self.last_attack = time()
        self.left_anim = pyganim.PygAnimation(ANIMATION_LEFT)
        self.left_anim.play()
        self.jump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.jump.play()
        self.ground = False
        self.state = 1

    def attack_player(self, group):
        for sprite in group:
            if pygame.sprite.collide_rect(sprite, self):
                if round(time()) - round(self.last_attack) >= self.time_attack:
                    if sprite.health <= 15:
                        sprite.damage(sprite.health)
                    elif sprite.health <= 50 and self.health <= 150:
                        sprite.damage(sprite.health - 1)
                    elif self.health <= 250:
                        sprite.damage(35)
                    else:
                        sprite.damage(5)
                    self.last_attack = time()
                    self.time_attack = choice(ATTACK_TIMES)
                    self.attack = True

    def collide_y(self, group):
        for sprite in group:
            if pygame.sprite.collide_rect(sprite, self):
                if self.speed_y > 0:
                    self.ground = True
                    self.speed_y = 0
                    self.rect.bottom = sprite.rect.top
            else:
                self.ground = False

    def draw_hp(self, surface, hp):
        pygame.draw.rect(surface, pygame.Color("red"), (150, 50, hp, 20))
        self.draw_text(surface, "Troll health {}%".format(round(self.health)))

    def damage(self):
        if round(time()) - round(self.last_hurt) >= 3:
            self.sounds["hurtT"].stop()
            self.sounds["hurtT"].play()
            self.health -= 50
            self.last_hurt = time()

    def update(self, collide_group, player_group, surface):
        if self.rect.colliderect((0, 0, 900, 640)) == 1 and self.alive():
            self.draw_hp(surface, self.health)
            if self.health <= 0:
                self.kill()
            if self.attack and time() - self.anim_attack_time <= 2:
                self.jump.blit(surface, (self.rect.x - 80, self.rect.y - 260))
            else:
                self.attack = False
                self.anim_attack_time = time()
            if not self.attack:
                if self.speed_x > 0:
                    self.right_anim.blit(surface, (self.rect.x - 40, self.rect.y - 90))
                elif self.speed_x < 0:
                    self.left_anim.blit(surface, (self.rect.x - 40, self.rect.y - 90))
                else:
                    self.stay_anim.blit(surface, (self.rect.x - 40, self.rect.y - 90))

            self.speed_x = -SPEED

            if not self.ground:
                self.speed_y += GRAVITY

            self.rect.y += self.speed_y
            self.collide_y(collide_group)

            if self.state < 250:
                self.rect.x += self.speed_x
            else:
                self.speed_x = 0
                self.state = 250
            self.state += 1
            self.attack_player(player_group)
        if self.health < 350:
            self.health += 0.05

    def reload(self):
        self.kill()

    def draw_text(self, surface, text):
        font = pygame.font.Font("CloisterBlack.ttf", 19)
        text = font.render(text, 1, pygame.Color("white"))
        text_x, text_y = 250 + 150, 50
        surface.blit(text, (text_x, text_y))
