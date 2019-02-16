import pygame


class Background(pygame.sprite.Sprite):
    bg = pygame.image.load("data/bg2.png")

    def __init__(self, group,):
        super().__init__(group)
        self.image = Background.bg
        self.rect = self.image.get_rect()

    def draw(self, surface, x, y):
        self.image.blit(surface, (x, y))
