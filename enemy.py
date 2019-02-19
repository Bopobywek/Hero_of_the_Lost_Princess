import os
from time import time
from random import choice

import pygame
import pyganim

ATTACK_TIMES = [3, 5]
GRAVITY = 0.5
SPEED = 5

GOLEM_ATTACK = [(pygame.transform.scale(pygame.image.load(os.path.join("data/enemy/attack", i)), (127, 106)), 100)
                for i in os.listdir("data/enemy/attack")] + [(pygame.transform.scale(pygame.image.load(
                                                                                     os.path.join("data/enemy/attack",
                                                                                                  i)), (127, 106)), 100)
                                                             for i in os.listdir("data/enemy/attack")][:-1:-1]

GOLEM_STAY = [(pygame.transform.scale(pygame.image.load(os.path.join("data/enemy/idle-walk", i)), (119, 96)), 80)
                for i in os.listdir("data/enemy/idle-walk")] + [(pygame.transform.scale(pygame.image.load(os.path.join(
                                                                                         "data/enemy/idle-walk", i)),
                                                                                        (119, 96)), 80)
                                                                for i in os.listdir("data/enemy/idle-walk")][:-1:-1]


class Enemy(pygame.sprite.Sprite):

    def __init__(self, group, x, y, w, h):
        super().__init__(group)
        self.attack = False
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.rect.x, self.rect.y = x, y
        self.speed_y = 0
        self.last_hurt = time()
        self.last_attack = time()
        self.time_attack = choice(ATTACK_TIMES)
        self.health, self.start_hp = 300, 300
        self.speed_x = 0
        self.ground = False

    def attack_player(self, group):
        for sprite in group:
            if pygame.sprite.collide_rect(sprite, self):
                if round(time()) - round(self.last_attack) >= self.time_attack:
                    if sprite.health <= 15:
                        sprite.damage(sprite.health)
                    elif sprite.health <= 50 and self.health <= 150:
                        sprite.damage(sprite.health - 1)
                    elif self.health <= 150:
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
        pygame.draw.rect(surface, pygame.Color("red"), (self.rect.x,
                                                        self.rect.y - 20,
                                                        self.rect.width * (self.health / self.start_hp),
                                                        20))
        self.draw_text(surface, "{}%".format(round(self.health)),
                       self.rect.x, self.rect.y - 20)

    def damage(self):
        if round(time()) - round(self.last_hurt) >= 2:
            self.health -= 50
            self.last_hurt = time()
            if self.health < 0:
                self.health = 0

    def draw_text(self, surface, text, x, y):
        font = pygame.font.Font("CloisterBlack.ttf", 19)
        text = font.render(text, 1, pygame.Color("white"))
        text_x, text_y = x + self.rect.width // 2 - text.get_width() // 2, y
        surface.blit(text, (text_x, text_y))

    def update(self, collide_group, player_group, surface, at):
        pass

    def reload(self):
        self.kill()


class Golem(Enemy):

    def __init__(self, group, x, y, w, h):
        super().__init__(group, x, y, w, h)
        self.attack_anim = pyganim.PygAnimation(GOLEM_ATTACK)
        self.attack_anim.play()
        self.anim_attack_time = time()
        self.stay = pyganim.PygAnimation(GOLEM_STAY)
        self.stay.play()

    def update(self, collide_group, player_group, surface, at):
        if self.rect.colliderect((0, 0, 900, 640)) == 1 and self.alive():
            self.draw_hp(surface, self.health)
            if self.attack and time() - self.anim_attack_time <= 2:
                self.attack_anim.blit(surface, (self.rect.x - 17, self.rect.y - 10))
            else:
                self.attack = False
                self.anim_attack_time = time()
            if not self.attack:
                self.stay.blit(surface, (self.rect.x - 9, self.rect.y))
            if self.health <= 0:
                self.kill()
            if at:
                self.health -= 50

            self.speed_x = -SPEED

            if not self.ground:
                self.speed_y += GRAVITY

            self.rect.y += self.speed_y
            self.collide_y(collide_group)

            self.attack_player(player_group)

        if self.health < 100:
            self.health += 0.05

