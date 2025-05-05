import pygame

class Coin:

    def __init__(self, x, y, scale=1, angle=0):
        self.single_coin_path = "Assets/Coin.png"
        self.pile_coin_path = "Assets/Pile.png"
        self.path = "Assets/Coin.png"
        self.x = x
        self.y = y
        self.scale = scalel
        self.coin_pile = coin_pile
        self.image_path = self.pile_coin_path if self.coin_pile else self.singe_coin_path
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def set_coin_pile(self, is_pile):
        self.coin_pile = is_pile
        self.image_path = self.pile_coin_path if self.set_coin_pile else self.single_coin_path
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.iamge.get_width() * self.scale), int(self.image.get_height())))
