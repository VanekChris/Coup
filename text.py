import pygame

class DrawText:

    def __init__(self, text, color, font_size, x, y, w, h, screen):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.SysFont(None, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        screen.blit(self.image, self.rect.center)
