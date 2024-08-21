import pygame
import sys
import random

from card import Card
from player import Player
from coin import Coin
from text import DrawText

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width, self.height = screen.get_size()
        self.run = True
        self.game_over = False
        self.card_names = []
        self.temp_deck = [['Ambassador', 'Assassin', 'Duke', 'Captain', 'Contessa'] for i in range(3)]
        self.deck = self.temp_deck[0] + self.temp_deck[1] + self.temp_deck[2]
        self.removed_deck = []
        self.players = []
        self.shuffle = 0
        self.game_coins = 72
        self.create_players()
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.player_turn_made = False
        self.target_player_index = False
        self.target_player = None
        self.response_order = list(self.players)

    def create_players(self):
        player_names = ["player 1", "player 2", "player 3", "player 4", "player 5", "player 6"]
        block_keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h]
        positions = [(100 + i * 200, 500) for i in range(6)]
        for i, name in enumerate(player_names):
            player = Player(name, block_keys[i], positions[i][0], positions[i][1])
            player.coins = 2
            self.game_coins -= 2
            player.cards = [Card(self.deck.pop(), False), Card(self.deck.pop(), False)]
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
            elif event.key == pygame.K_8:
                return 8 # block

    def wait_for_response(self, target_player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        return 'accept'
                    elif event.key == pygame.K_b:
                        return 'block'
                    elif event.key == pygame.K_c:
                        return 'challenge'

    def get_current_player(self):
        return self.response_order[0]

    def rotate_players(self):
        self.response_order.append(self.response_order.pop(0))

    def wait_for_any_response(self):
        responses = {player: None for player in self.players if player != self.current_player}
        
        while not all(choice == 'accept' for choice in responses.values()):
        
            for player in self.response_order:
                if player == self.current_player:
                    continue

                response = None
        
                while response is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_a:
                                response = 'accept'
                            elif event.key == pygame.K_c:
                                response = 'challenge'
                        
                    if response:
                        self.draw_action_text(player, response)
                        if response =='challenge':
                            return 'challenge'
                        responses[player] = response
                    
        return 'accept'

    def draw_action_text(self, player, text):
        player_index = self.players.index(player)
        player_x = 100 + player_index * 200
        player_y = 500
        draw_action = DrawText(text, 'black', 30, player_x, player_y - 50, 100, 50, self.screen)
        pygame.display.update()

    def player_accept_challenge(self, player, response):
        if response == 'block':
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.clear_text()
                            self.draw_action_text(self.current_player, 'accept')
                            pygame.display.update()
                            return 'accept'
                        elif event.key == pygame.K_c:
                            self.clear_text()
                            self.draw_action_text(self.current_player, 'challenge')
                            pygame.display.update()
                            return 'challenge'

    def clear_text(self):
        green = (39, 119, 20)
        self.screen.fill(green)
        pygame.display.update()

    def player_turns(self, action):
        if not self.player_turn_made and action:
            player = self.current_player

            if action == 1 and player.coins < 10:
                player.income()
                self.game_coins -= 1
                self.player_turn_made = True

            elif action == 2 and player.coins < 10:
                self.draw_action_text(player, 'FOREIGN AID')
                response = self.wait_for_any_response()
                if response == 'accept':
                    player.foreign_aid()
                    self.game_coins -= 2
                    self.player_turn_made = True
                elif response == 'challenge':
                    pass

            elif action == 3 and player.coins < 10:
                self.draw_action_text(player, 'TAX')
                response = self.wait_for_any_response()
                if response == 'accept':
                    player.tax()
                    self.game_coins -= 3
                    self.player_turn_made = True
                elif response == 'challenge':
                    pass

            elif action == 4 and player.coins < 10:
                target = self.select_target(player)
                if target and target.coins >= 2:
                    self.draw_action_text(player, 'STEAL')
                    self.draw_action_text(target, 'TARGET')
                    response = self.wait_for_response(target)
                    if response == 'block':
                        self.draw_action_text(target, 'BLOCK')
                        response = self.player_accept_challenge(self.current_player, response)
                        if response == 'accept':
                            self.player_turn_made = True
                        #else:
                            #challenge()
                    elif response == 'challenge':
                        # challenge logic
                        pass
                    elif response == 'accept':
                        self.draw_action_text(target, 'ACCEPT')
                        player.steal(target)
                        target.coins -= 2
                        self.player_turn_made = True
                        
            elif action == 5 and (3 <= player.coins <= 10):
                # I assassinate someone
                target = self.select_target(player)
                if target: # picked a target
                    self.draw_action_text(self.current_player, 'assassinate')
                    response = self.wait_for_response(target)
                    if response == 'block': # target blocks (they have contessa)
                        self.draw_action_text(target, 'BLOCK')
                        response = self.player_accept_challenge(self.current_player, response)
                        if response == 'accept': # I accept
                            self.current_player.coins -= 3
                            self.game_coins += 3
                            self.player_turn_made = True
                        elif response == 'challenge':
                            target.has_card('contessa')
                            # check if contessa is in the hand or not
                            #if in hand -> current player loses a card
                            # if not in hand -> target loses a card
                    elif response == 'accept':
                        player.assassinate(target)
                        self.game_coins += 3
                        removed_card = target.cards.pop()
                        self.removed_deck.append(removed_card)
                        self.player_turn_made = True

            elif action == 6:
                self.draw_action_text(player, 'EXCHANGE')
                response = self.wait_for_any_response()
                if response == 'accept':
                    self.exchange_cards()
                    self.player_turn_made = True
                elif response == 'challenge':
                    pass

            elif action == 7 or player.coins >= 10:
                target = self.select_target(player)
                if target:
                    player.coup(target)
                    self.game_coins += 7
                    removed_card = target.cards.pop()
                    self.removed_deck.append(removed_card)
                    self.player_turn_made = True
            
            if self.player_turn_made:
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                self.current_player = self.players[self.current_player_index]
                self.player_turn_made = False

    def exchange_cards(self):

        deck_cards = [Card(self.deck.pop(), False), Card(self.deck.pop(), False)]
        player_cards = self.current_player.cards

        selected_index = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % 4
                    elif event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % 4
                    elif event.key == pygame.K_UP:
                        if selected_index < 2:
                            player_cards[selected_index], deck_cards[0] = deck_cards[0], player_cards[selected_index]
                        else:
                            player_cards[selected_index - 2], deck_cards[1] = deck_cards[1], player_cards[selected_index - 2]
                    elif event.key == pygame.K_DOWN:
                        if selected_index < 2:
                            player_cards[selected_index], deck_cards[1] = deck_cards[1], player_cards[selected_index]
                        else:
                            player_cards[selected_index - 2], deck_cards[0] = deck_cards[0], player_cards[selected_index - 2]
                    elif event.key == pygame.K_RETURN:
                        self.deck.extend([str(card)for card in deck_cards])
                        return
                    self.render_exchange_cards(player_cards, deck_cards, selected_index)
            pygame.display.update()
            self.clock.tick(60)

    def render_exchange_cards(self, player_cards, deck_cards, selected_card):
        green = (39, 119, 20)
        self.screen.fill(green)

        start_x, start_y = 100, 600
        deck_start_x, deck_start_y = 100, 300
        card_offset = 100

        for index, card in enumerate(player_cards):
            card_x = start_x + index * card_offset
            if index == selected_card:
                pygame.draw.rect(self.screen, "yellow", pygame.Rect(card_x - 10, start_x - 10, 80, 120), 3)
            card.draw(self.screen, card_x, start_y, scale=0.1, angle=0)

        for index, card in enumerate(deck_cards):
            card_x = deck_start_x + index * card_offset
            if index + 2 == selected_card:
                pygame.draw.rect(self.screen, "yellow", pygame.Rect(card_x - 10, start_x - 10, 80, 120), 3)
            card.draw(self.screen, card_x, deck_start_y, scale=0.1, angle=0)

        pygame.display.update()

    def swap_card(self, selected_card_index):
        self.current_player.cards[0] = self.flipped_cards[selected_card_index]
        self.flipped_cards.pop(selected_card_index)
    
    def select_target(self, current_player):
        target = None
        self.target_player = target
        while not target:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    target_index = event.key - pygame.K_1
                    if 0 <= target_index < len(self.players) and self.players[target_index] != self.current_player:
                        return self.players[target_index]
                        break

            self.render()
            pygame.display.update()
            self.clock.tick(60)
        return target

    def render(self):
        green = (39, 119, 20)
        self.screen.fill(green)
        self.display_player_cards()
        self.display_player_coins()
        self.pile()
        self.display_deck()
        self.highlight_current_player()
        self.display_removed_cards()

        if self.target_player:
            target_text = DrawText(f"Target", "white", 40, self.width // 2, 50, 0, 0, self.screen)

    def display_deck(self):
        deck_x = self.width // 2 - 300
        deck_y = 200
        card_spacing = 20

        for i, card_name in enumerate(self.deck):
            card_x = deck_x - (i % 5) * card_spacing
            card_y = deck_y + (i // 5) * card_spacing
            card = Card(card_name, True)
            card.draw(self.screen, card_x, card_y, scale=0.15, angle=0)

    def display_removed_cards(self):
        deck_x = self.width // 2 - 300
        deck_y = 20
        card_spacing = 50

        for index, card in enumerate(self.removed_deck):
            card_x = deck_x + (index * card_spacing)
            card_y = deck_y
            card.draw(self.screen, card_x, card_y, scale=0.15, angle=0)

    def pile(self):
        pile_x = self.width // 2
        pile_y = 200
        pile_scale = 0.2
        for i in range(self.game_coins):
            offset_x = (i % 6) * 30
            offset_y = (i // 6) * 30
            coin_x = pile_x - (self.game_coins // 2) * -5 + offset_x
            coin_y = pile_y + offset_y
            coin = Coin(coin_x, coin_y, scale=0.1, angle=0)
            coin.draw(self.screen)

    def display_player_coins(self):
        coin_spacing = 30
        start_x, start_y = 100, 550

        for index, player in enumerate(self.players):
            player_x = start_x + index * 200
            for coin_index in range(player.coins):
                coin_x = player_x + (coin_index * coin_spacing) % (200)
                coin_y = start_y + (coin_index * coin_spacing) // (200) * 20
                coin = Coin(coin_x, coin_y, scale=0.1, angle=0)
                coin.draw(self.screen)

    def display_player_cards(self):
        start_x, start_y = 100, 600
        offset_x = 200
        card_offset_x = 50

        for index, player in enumerate(self.players):
            player_x = start_x + index * offset_x
            for card_index, card in enumerate(player.cards):
                card_x = player_x + card_index * card_offset_x
                card.draw(self.screen, card_x, start_y, scale=0.1, angle=0)

    def restart_game(self):
        pass

    def highlight_current_player(self):
        start_x, start_y = 100, 500
        player_x = start_x + self.current_player_index * 200
        pygame.draw.rect(self.screen, "red", pygame.Rect(player_x - 10, start_y - 10, 220, 60), 2)

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