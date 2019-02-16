import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, group, image_name, second_img_name, x, y, sound_name, button_name):
        super().__init__(group)
        self.button_name = button_name
        self.sound = pygame.mixer.Sound("data/music/{}".format(sound_name))
        self.second_image = pygame.image.load("data/{}".format(second_img_name))
        self.first_image = pygame.image.load("data/{}".format(image_name))
        self.image = self.first_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pressed = False

    def draw(self, surface):
        surface.blit(self.image(self.rect.x, self.rect.y))

    def update(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if self.image != self.second_image:
                    self.sound.play(0)
                self.image = self.second_image
            else:
                self.image = self.first_image
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True

    def state(self):
        return self.pressed
