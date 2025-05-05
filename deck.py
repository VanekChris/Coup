import pygame
import random

from card import Card

class Deck:

    def __init__(self, width, screen):
        self.temp_deck = [['Ambassador', 'Assassin', 'Duke', 'Captain', 'Contessa'] for i in range(3)]
        self.card_names = self.temp_deck[0] + self.temp_deck[1] + self.temp_deck[2]
        self.deck = []
        self.removed_deck = []
        self.width = width
        self.screen = screen

    def __str__(self):
        return f"{self.deck}"

    def create_deck(self):

        for name in self.card_names:
            card = Card(name, back_side=False)
            self.deck.append(card)
        self.shuffle_deck()
        return self.deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        if self.deck:
            return self.deck.pop()
        return None
    
    def remove_card(self, card):
        self.removed_deck.append(card)

    def return_card(self, card):
        self.deck.append(card)
        self.shuffle_deck()

    def display_deck(self):
        deck_x = self.width // 2 - 300
        deck_y = 200
        card_spacing = 20

        for i, card in enumerate(self.deck):
            card_x = deck_x - (i % 5) * card_spacing
            card_y = deck_y + (i // 5) * card_spacing
            card.back_side = True
            card.draw(self.screen, card_x, card_y, scale=0.15, angle=0)

    def display_removed_cards(self):
        deck_x = self.width // 2 - 300
        deck_y = 20
        card_spacing = 50

        for index, card in enumerate(self.removed_deck):
            card_x = deck_x + (index * card_spacing)
            card_y = deck_y
            card.back_side = False
            card.draw(self.screen, card_x, card_y, scale=0.15, angle=0)
