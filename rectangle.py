import pygame

class Rectangle:

    def __init__(self, x, y, w, h, color, thickness):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.thickness = thickness

    def update(self, x, y):
        self.rect.topleft = (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.thickness)
