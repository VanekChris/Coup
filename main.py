import pygame
import sys

from game import Game
from menu import MenuScreen

pygame.init()

WIDTH = 1400
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coup")
clock = pygame.time.Clock()

def main():
    while True:
        #menu = MenuScreen(SCREEN)
        #menu.run_menu()
        #if not menu.run:
        game = Game(SCREEN)
        game.run_game()

if __name__=="__main__":
    main()
