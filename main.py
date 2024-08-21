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

"""
created assets ✅
dealt cards ✅
dealt coins ✅
Displayed coins ✅    
Displayed Deck ✅
Make turns for each player, income, foreign aid ✅
Steal works ✅
ensure that each turn for the player visibly ends before the next one ✅
Assasinate works ✅
coup works ✅
Ensure that lost cards remain on screen. Maybe at the top. ✅

challenge function(s)  card names seem to be a problem.
declare winner
restart game
"""