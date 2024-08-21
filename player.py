import pygame

class Player:
    def __init__(self, name, block_key, x, y):
        self.name = name
        self.cards = []
        self.coins = 0
        self.stats = ""
        self.max_coins = 10
        self.block = False
        self.block_key = block_key
        self.accept = pygame.K_SPACE
        self.x = x
        self.y = y

    def assassinate(self, target):
        
        if 3 <= self.coins <= self.max_coins:
            self.coins -= 3

        # block statement
        # challenge statement

    def exhange_cards(self, deck):
        pass

    def steal(self, target):
        if self.coins < self.max_coins:
            self.coins += 2
        
        # elif condition:
            #player has captain or ambasador
        
        else:
            
            # challenge from other player
            pass 

    def tax(self):
        if self.coins < self.max_coins:
            self.coins += 3
        else:
            # challenge from other player
            pass

    def income(self):
        if self.coins < self.max_coins:
            self.coins += 1

    def foreign_aid(self):
        if self.coins < self.max_coins:
            self.coins += 2
        else:
            # Duke block
            pass
        
    def coup(self, target):
        if self.coins >= 7:
            self.coins -= 7

    def challenge(self, target):
        pass

    def block(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.block_key:
                return True
        return False

    def accept(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.accept:
                return True
        return False

    def has_card(self, card_name):
        return any(card.name == card_name for card in self.cards)