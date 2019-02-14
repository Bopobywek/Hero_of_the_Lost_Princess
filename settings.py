import pygame


class Settings(object):

    def __init__(self, surface):
        self.surface = surface
        self.background = pygame.image.load("data/setting_menu.png")
        self.running = True
        self.rects = dict()
        self.create_rects_with_text("To main menu", (0, 0))
        self.clicked_area = None

    def update(self):
        self.draw()

    def draw(self):
        if self.running:
            self.surface.blit(self.background, (0, 0))
            for key, val in self.rects.items():
                if self.clicked_area is not None:
                    if val.collidepoint(self.clicked_area):
                        self.clicked_handler()
                        print("closed")
                pygame.draw.rect(self.surface, pygame.Color("white"), val)
                self.surface.blit(key, (val.x, val.y + 1))

    def create_rects_with_text(self, text, coords):
        text_obj = self.draw_text(text)
        x, y = coords
        self.rects[text_obj] = pygame.Rect((x, y, text_obj.get_width(), text_obj.get_height()))

    def clicked(self, pos):
        self.clicked_area = pos

    def clicked_handler(self):
        self.running = False
        self.clicked_area = None

    def draw_text(self, text):
        font = pygame.font.Font("CloisterBlack.ttf", 30)
        text = font.render(text, 1, pygame.Color("Black"))
        return text
