import pygame


class Cursor(pygame.sprite.Sprite):
    image = pygame.image.load("data/cursor.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()
