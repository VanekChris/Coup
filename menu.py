import pygame
import sys

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.run = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.run = False
                pygame.quit()
                sys.exit()

    def draw(self):
        green = (39, 119, 20)
        self.screen.fill(green)

    def run_menu(self):
        while self.run:
            self.handle_events()
            self.draw()
            pygame.display.update()
