import pygame


GRAVITY = 0.5
SPEED = 2


class Princess(pygame.sprite.Sprite):
    princess_png = pygame.image.load("data/princess/princess.png")
    princess_png = pygame.transform.scale(princess_png, (40, 70))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Princess.princess_png
        self.rect = pygame.Rect((x, y, 40, 70))
        self.rect.x, self.rect.y = x, y
        self.speed_y = 0
        self.speed_x = -1
        self.ground = False
        self.state = 1

    def collide_y(self, group):
        for sprite in group:
            if pygame.sprite.collide_rect(sprite, self):
                if self.speed_y > 0:
                    self.ground = True
                    self.speed_y = 0
                    self.rect.bottom = sprite.rect.top
            else:
                self.ground = False

    def update(self, collide_group):
        if self.state % 10 == 0:
            self.speed_x = -self.speed_x
            self.state = 1
        if not self.ground:
            self.speed_y += GRAVITY

        self.rect.y += self.speed_y
        self.collide_y(collide_group)

        self.rect.x += self.speed_x * SPEED
        self.state += 1

    def reload(self):
        self.kill()
