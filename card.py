import pygame

class Card:

    def __init__(self, card_type, back_side=False):

        self.card_type = card_type
        self.back_side = back_side
        path = "Assets/" + card_type + ".png"
        self.image = pygame.image.load(path).convert_alpha()

    def draw(self, screen, x, y, scale=1, angle=0):
        if self.back_side:
            draw_image = pygame.image.load("Assets/Back.png").convert_alpha()
        else:
            draw_image = self.image

        width = int(draw_image.get_width() * scale)
        height = int(draw_image.get_height() * scale)
        draw_image = pygame.transform.scale(draw_image, (width, height))
        screen.blit(draw_image, (x, y))
