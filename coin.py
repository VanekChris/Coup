import pygame

class Coin:

    def __init__(self, x, y, scale=1, angle=0):
        self.path = "Assets/Coin.png"
        self.x = x
        self.y = y
        self.scale = scale
        self.image = pygame.image.load(self.path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))