import pygame
import sys
import random

from card import Card
from player import Player
from coin import Coin
from text import DrawText
from deck import Deck
from rectangle import Rectangle

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width, self.height = screen.get_size()
        self.run = True
        self.game_over = False
        self.players = []
        self.shuffle = 0
        self.game_coins = 72  
        self.player_turn_made = False
        self.target_player_index = False
        self.target_player = None
        self.response_order = list(self.players)
        self.block = False
        self.removed_players = []
        self.deck = Deck(self.width, self.screen)
        self.deck.create_deck()
        self.deck.removed_deck
        self.create_players()
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]

    def remove_players(self):
        for player in self.players:
            if len(player.cards) == 0 and not player.eliminated:
                player.eliminated = True
                self.return_coins()
                self.removed_players.append(player)

    def declare_winner(self, player):
        if len(self.removed_players) == 5:
            winner = player
            self.draw_action_text(winner, f"winner!", 0)
            pygame.display.update()
            pygame.time.delay(3000)
            self.restart_game()
            return

    def create_players(self):
        player_names = ["player 1", "player 2", "player 3", "player 4", "player 5", "player 6"]
        block_keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h]
        positions = [(100 + i * 200, 500) for i in range(6)]
        for i, name in enumerate(player_names):
            player = Player(name, block_keys[i], positions[i][0], positions[i][1], self, self.deck)
            player.coins = 2
            self.game_coins -= 2
            player.cards = [self.deck.draw_card(), self.deck.draw_card()]
            self.players.append(player)

    def process_events(self):
        events = pygame.event.get()
        action = None
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            action = self.input_number(event)
            if action:
                self.player_turns(action)
                
        pygame.display.update()
        self.clock.tick(60)
        return events

    def input_number(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return 1 # income
            elif event.key == pygame.K_2:
                return 2 # foreign aid
            elif event.key == pygame.K_3:
                return 3 # tax
            elif event.key == pygame.K_4:
                return 4 # steal
            elif event.key == pygame.K_5:
                return 5 # assassinate
            elif event.key == pygame.K_6:
                return 6 # exchange cards
            elif event.key == pygame.K_7:
                return 7 # coup

    def get_current_player(self):
        return self.response_order[0]

    def rotate_players(self):
        self.response_order.append(self.response_order.pop(0))

    def draw_action_text(self, player, text, offset):
        player_index = self.players.index(player)
        player_x = 125 + player_index * 200 + offset
        player_y = 800
        draw_action = DrawText(text, 'black', 30, player_x, player_y - 50, 100, 50, self.screen)
        pygame.display.update()

    def clear_text(self, player):
        green = (39, 119, 20)
        player_index = self.players.index(player)
        player_x = player.x
        player_y = player.y + 250
        clear_rect = pygame.Rect(player_x, player_y, 150, 50)
        pygame.draw.rect(self.screen, green, clear_rect)

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        self.current_player.turn_made = False    

    def player_eliminated(self):
        if len(self.current_player.cards) == 0: # while loop?
            self.game_coins += self.current_player.coins
            self.current_player.coins = 0
            self.current_player.turn_made = True
            self.next_player()
            
    def swap_cards(self, player, card):
        self.deck.deck.append(card)
        player.cards.remove(card)
        random.shuffle(self.deck.deck)
        new_card = self.deck.deck.pop()
        player.cards.append(new_card)

    def resolve_challenge(self, player, responder, required_cards):
        found_card = any(card.card_type in required_cards for card in player.cards)

        if found_card:

            for card in player.cards:
                if card.card_type in required_cards:
                    self.swap_cards(player, card)
                    break
            remove_card = responder.cards.pop()
            self.deck.remove_card(remove_card)
            player.change_card = True
        else:
            remove_card = player.cards.pop()
            self.deck.removed_deck.append(remove_card)
            self.player_turn_made = True
            player.change_card = False
        
        return found_card

    def return_coins(self):
        for player in self.removed_players:
            self.game_coins += player.coins
            player.coins = 0

    def player_turns(self, action):
        
        
        self.remove_players()
        self.player_eliminated()

        player = self.current_player
        self.declare_winner(player)

        if not player.turn_made and action and len(player.cards) > 0:
            
            # income
            if action == 1 and player.coins < 10:
                player.income(self)

            # foreign aid
            elif action == 2 and player.coins < 10:
                player.foreign_aid(self)

            # tax   
            elif action == 3 and player.coins < 10:
                player.tax(self)
            
            # steal
            elif action == 4 and player.coins < 10:
                player.steal(self)
           
            # assassinate
            elif action == 5 and (3 <= player.coins <= 10):
                player.assassinate(self)
           
            # exchange 
            elif action == 6 and player.coins <= 10:
                player.exchange_cards(self.deck, self)
            
            # coup
            elif action == 7 and player.coins >= 7:
                player.coup(self)
            
        if player.turn_made:
            self.next_player()

    def exchange_cards(self): 

        deck_cards = [self.deck.deck.pop(), self.deck.deck.pop()]
        player_cards = self.current_player.cards
        selected_index = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if len(player_cards) == 2:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            selected_index = (selected_index - 1) % 4
                        elif event.key == pygame.K_RIGHT:
                            selected_index = (selected_index + 1) % 4
                        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            if selected_index < 2:
                                player_cards[selected_index], deck_cards[selected_index] = deck_cards[selected_index], player_cards[selected_index]
                            else:
                                idx = selected_index - 2
                                player_cards[idx], deck_cards[idx] = deck_cards[idx], player_cards[idx]
                        
                        elif event.key == pygame.K_RETURN:
                            self.deck.deck.extend(deck_cards)
                            return
                        
                elif len(player_cards) == 1:

                    temp_cards = [player_cards[0], deck_cards[0], deck_cards[1]]
                    selected_index = 1
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            deck_cards[1], deck_cards[0] = deck_cards[0], deck_cards[1]
                        elif event.key == pygame.K_RIGHT:
                            deck_cards[0], deck_cards[1] = deck_cards[1], deck_cards[0]
                        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            player_cards[0], deck_cards[0] = deck_cards[0], player_cards[0]
                                
                        elif event.key == pygame.K_RETURN:
                            self.deck.deck.extend(deck_cards)
                            return
                self.render_exchange_cards(player_cards, deck_cards, selected_index)
            pygame.display.update()
            self.clock.tick(60)

    def render_exchange_cards(self, player_cards, deck_cards, selected_card):
        green = (39, 119, 20)
        self.screen.fill(green)

        # fix selecting issue. Highlited cards are not always swapped correctly.

        card_width = 100
        card_height = 150
        spacing = 200
        start_x = 100
        y_player = 300
        y_deck = 500

        all_cards = player_cards + deck_cards

        start_x, start_y = 100, 600
        deck_start_x, deck_start_y = 100, 300
        card_offset = 200

        for index, card in enumerate(player_cards):
            card_x = start_x + index * card_offset
            DrawText("Player Cards", "black", 30, 625, 450, 50, 50, self.screen)
            card.draw(self.screen, card_x + 400, start_y - 100, scale=0.2, angle=0)
            card.back_side = False

            if index == selected_card:
                selector = Rectangle(card_x + 400, start_y - 100, 177, 260, "red", 2)
                selector.draw(self.screen)


        for index, card in enumerate(deck_cards): 
            card_x = deck_start_x + index * card_offset
            DrawText("Deck Cards", "black", 30, 625, 50, 50, 50, self.screen)
            card.draw(self.screen, card_x + 400, deck_start_y - 200, scale=0.2, angle=0)
            card.back_side = False

            if (index + len(player_cards)) == selected_card:
                deck_select = Rectangle(card_x + 400, start_y - 500, 177, 260, "blue", 2)
                deck_select.draw(self.screen)
        pygame.display.update()

    def swap_card(self, selected_card_index):
        self.current_player.cards[0] = self.flipped_cards[selected_card_index]
        self.flipped_cards.pop(selected_card_index)
    
    def select_target(self):  # fix text display
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    target_index = event.key - pygame.K_1
                    if 0 <= target_index < len(self.players):
                        target = self.players[target_index]
                        #if target != current_player and not target.eliminated:
                        return target

            pygame.display.update()
            self.clock.tick(60)

    def render(self):
        green = (39, 119, 20)
        self.screen.fill(green)
        self.display_player_cards()
        self.display_player_coins()
        self.pile()
        self.deck.display_deck()
        self.highlight_current_player()
        self.deck.display_removed_cards()
        self.display_controls()

        if self.target_player:
            target_text = DrawText(f"Target", "white", 40, self.width // 2, 50, 0, 0, self.screen)

    def pile(self):
        pile_x = self.width // 2
        pile_y = 200
        pile_scale = 0.15
        coins_per_row = 10
        pile_spacing_x = 35
        pile_spacing_y = 40

        pile_images = self.game_coins // 2

        for i in range(pile_images):
            offset_x = (i % coins_per_row) * pile_spacing_x
            offset_y = (i // coins_per_row) * pile_spacing_y
            coin_x = pile_x + offset_x
            coin_y = pile_y + offset_y
            coin_pile = Coin(coin_x, coin_y, scale=pile_scale, angle=0, coin_pile=True)
            coin_pile.draw(self.screen)

    def display_player_coins(self):
        start_x, start_y = 100, 480

        for index, player in enumerate(self.players):
            player_x = start_x + index * 200
            coin_x = player_x + 20
            coin_y = start_y + 60
            coin = Coin(coin_x, coin_y, scale=0.1, angle=0)
            coin.draw(self.screen)

            coin_count_x = coin_x + 50
            coin_count_y = coin_y + 7
            font = pygame.font.Font(None, 36)
            coin_text = font.render(str(player.coins), True, "black")
            self.screen.blit(coin_text, (coin_count_x, coin_count_y))

    def display_player_cards(self):
        start_x, start_y = 100, 600
        offset_x = 200
        card_offset_x = 50

        for index, player in enumerate(self.players):
            player_x = start_x + index * offset_x
            for card_index, card in enumerate(player.cards):
                card_x = player_x + card_index * card_offset_x
                card.draw(self.screen, card_x, start_y, scale=0.1, angle=0)

        for player in self.players:
            for card in player.cards:
                if player == self.current_player:
                    card.back_side = False
                else:
                    card.back_side = True

    def restart_game(self):

        self.removed_players = []
        self.game_coins = 50
        self.deck.deck = []
        self.deck.create_deck()
        random.shuffle(self.deck.deck)
        self.deck.removed_deck = []

        for player in self.players:
            player.cards = []
            player.coins = 2
            player.eliminated = False
            player.turn_made = False
            player.cards.append(self.deck.draw_card())
            player.cards.append(self.deck.draw_card())

        self.current_player_index = 0
        self.current_player = self.players[0]

        self.run_game()

    def highlight_current_player(self):
        if len(self.current_player.cards) > 0:
            start_x, start_y = 100, 500
            player_x = start_x + self.current_player_index * 200
            highlight = Rectangle(player_x - 10, start_y + 90, 160, 150, "red", 2)
            highlight.draw(self.screen)

        elif len(self.current_player.cards) == 0:
            self.player_eliminated()

    def display_controls(self):
        DrawText("INCOME: 1", "black", 30, 50, 50, 50, 50, self.screen)
        DrawText("FOREIGN AID: 2", "black", 30, 50, 75, 50, 50, self.screen)
        DrawText("TAX: 3", "black", 30, 50, 100, 50, 50, self.screen)
        DrawText("STEAL: 4", "black", 30, 50, 125, 50, 50, self.screen)
        DrawText("ASSASSINATE: 5", 30, 30, 50, 150, 50, 50, self.screen)
        DrawText("EXCHANGE: 6", "black", 30, 50, 175, 50, 50, self.screen)
        DrawText("COUP: 7", "black", 30, 50, 200, 50, 50, self.screen)
        DrawText("ACCEPT: A", "black", 30, 50, 225, 50, 50, self.screen)
        DrawText("BLOCK: B", "black", 30, 50, 250, 50, 50, self.screen)
        DrawText("CHALLENGE: C", "black", 30, 50, 275, 50, 50, self.screen)
        DrawText("CONFIRM: RETURN", "black", 30, 50, 300, 50, 50, self.screen)

    def run_game(self):
        while self.run:
            events = self.process_events()
            self.render()
            if not self.game_over:
                pass
            
            else:
                pass
            pygame.display.update()
            self.clock.tick(60)

if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((1400, 800))
    game = Game(screen)
    game.run_game()
