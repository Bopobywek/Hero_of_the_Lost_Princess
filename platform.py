import os

import pygame

from princess import Princess
from boss import Troll
from enemy import Golem


class Platform(pygame.sprite.Sprite):
    image_platform = pygame.image.load("data/tile.png")

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Platform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class InvisiblePlatform(pygame.sprite.Sprite):

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.Surface((47, 47), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class LeftPlatform(pygame.sprite.Sprite):
    image_platform = pygame.image.load("data/tilel.png")

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = LeftPlatform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Coin(pygame.sprite.Sprite):
    image_platform = pygame.image.load("data/coin/coin_01.png")
    image_platform = pygame.transform.scale(image_platform, (47, 47))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Coin.image_platform
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class RightPlatform(pygame.sprite.Sprite):
    image_platform = pygame.image.load("data/tiler.png")

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = RightPlatform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class DestroyPlatform(pygame.sprite.Sprite):
    image_platform = pygame.image.load("data/tiled.png")

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = DestroyPlatform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Sign(pygame.sprite.Sprite):
    image_platform = pygame.image.load("data/10002.png")
    image_platform = pygame.transform.scale(image_platform, (47, 47))

    def __init__(self, group, x, y, text):
        super().__init__(group)
        self.image = Sign.image_platform
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.text = text


class BossPlatform(pygame.sprite.Sprite):
    image_platform = pygame.image.load("data/grid.png")
    image_platform = pygame.transform.scale(image_platform, (47, 47))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = BossPlatform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, boss_sprite):
        if not bool([x for x in boss_sprite]):
            self.kill()


class LevelPlatform(pygame.sprite.Sprite):

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.Surface((47, 47), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


def draw_level(filename, platfrom_h, platfrom_w, sprtie_groups):
    group_of_sprites, group_of_sprites_2, hero_sprite, princess_sprite, info_sprites, boss, enemy = sprtie_groups[0],\
                                                                                       sprtie_groups[1],\
                                                                                       sprtie_groups[2],\
                                                                                       sprtie_groups[3],\
                                                                                       sprtie_groups[4],\
                                                                                       sprtie_groups[5],\
                                                                                       sprtie_groups[6]
    fullname = os.path.join('data/levels', "{}.txt".format(filename))
    with open(fullname, mode="r") as level_in:
        level = [i.rstrip() for i in level_in.readlines()]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "-":
                Platform(group_of_sprites, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "?":
                InvisiblePlatform(group_of_sprites, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "l":
                LeftPlatform(group_of_sprites, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "r":
                RightPlatform(group_of_sprites, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "d":
                DestroyPlatform(group_of_sprites, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "|":
                LevelPlatform(group_of_sprites, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "0":
                BossPlatform(group_of_sprites, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "s":
                Sign(info_sprites, platfrom_w * x, platfrom_h * y, "123").add(group_of_sprites_2)
            elif level[y][x] == "c":
                Coin(group_of_sprites, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "P":
                Princess(princess_sprite, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "B":
                Troll(boss, platfrom_w * x, platfrom_h * y).add(group_of_sprites_2)
            elif level[y][x] == "@":
                Golem(enemy, platfrom_w * x - (110 - 47), platfrom_h * y - (96 - 47), 110, 96).add(group_of_sprites_2)
