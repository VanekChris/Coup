import pygame
import random

class Player:
    def __init__(self, name, block_key, x, y, game, deck):
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
        self.response = ''
        self.eliminated = False
        self.turn_made = False
        self.game = game
        self.deck = deck
        self.change_card = False
        self.reaction_text = ['ACCEPT', 'BLOCK', 'CHALLENGE']
        self.moves = ['INCOME', 'FOREIGN AID', 'TAX', 'STEAL', 'ASSASSINATE', 'EXCHANGE', 'COUP']
    
    def income(self, game):
        game.draw_action_text(self, self.moves[0], 0)
        if self.coins < self.max_coins:
            self.coins += 1
            game.game_coins -= 1
            self.turn_made = True

    def foreign_aid(self, game):
        game.draw_action_text(self, self.moves[1], -25)
        game.response_order = [p for p in game.players if p != game.current_player and not p.eliminated]
        
        responder, response = self.accept_or_block(game)

        if response == self.reaction_text[0]:
            game.game_coins -= 2
            self.coins += 2
        elif response == self.reaction_text[1]:
            self.block_play(responder, "Duke")
        self.turn_made = True

    def tax(self, game):
        game.draw_action_text(self, self.moves[2], +20)
        game.response_order = [p for p in game.players if p != game.current_player and not p.eliminated]
        responder, response = self.accept_or_challenge(game)
        if response == self.reaction_text[0]:
            game.game_coins -= 3
            self.coins += 3
                         
        elif response == self.reaction_text[2]: 
            if game.resolve_challenge(self, responder, 'Duke'):
                game.game_coins -= 3
                self.coins += 3

        self.turn_made = True

    def steal(self, game): 
        game.draw_action_text(self, self.moves[3], 0)
        
        target = game.select_target()
        if target and target.coins >= 2:
            game.draw_action_text(target, 'TARGET', 0)
            response = self.wait_for_any_response(target, self.game)

            if response == self.reaction_text[1]:
                game.clear_text(target)
                game.draw_action_text(target, self.reaction_text[1], 0)
                response = self.block_play(target, ["Duke", "Ambassador"])
                if response == self.reaction_text[0]:
                    game.clear_text(self)
                    game.draw_action_text(self, self.reaction_text[0], 0)
                    self.turn_made = True
                elif response == self.reaction_text[2]:
                    game.clear_text(self)
                    game.draw_action_text(self, self.reaction_text[2], -25)
                    if game.resolve_challenge(target, self, ["Captain", "Ambassador"]):
                        self.turn_made = True
                    else:
                        target.coins -= 2
                        self.coins += 2
            
            elif response == self.reaction_text[2]: # works
                if game.resolve_challenge(self, target, ['Captain']):
                    target.coins -= 2
                    self.coins += 2
                else:
                    self.turn_made = True

            elif response == self.reaction_text[0]: # works
                game.clear_text(target)
                game.draw_action_text(target, self.reaction_text[0], 0)
                target.coins -= 2
                self.coins += 2
        self.turn_made = True

    def assassinate(self, game):
        target = self.select_target(game)
        game.draw_action_text(self, self.moves[4], -25)
        if target: 
            game.draw_action_text(target, "TARGET", 0)
            self.coins -= 3
            game.game_coins += 3

            response = self.wait_for_any_response(target, self.game)

            if response == self.reaction_text[0]:
                game.clear_text(target)
                game.draw_action_text(target, self.reaction_text[0], 0)
                target.remove_random_card(target, game)

            elif response == self.reaction_text[2]:
                game.clear_text(target)
                game.draw_action_text(target, self.reaction_text[2], -25)
                found_assassin = any(card.card_type == 'Assassin' for card in self.cards)
                if not found_assassin:
                    self.remove_random_card(self, game)

                elif found_assassin:
                    if len(target.cards) == 1:
                        target.remove_random_card(target, game)
                        self.draw_new_card('assassin', game)

                    elif len(target.cards) == 2:
                        target.remove_random_card(target, self)
                        target.remove_random_card(target, self)
                        self.draw_new_card('assassin', self)

            elif response == self.reaction_text[1]:
                game.clear_text(target)
                game.draw_action_text(target, self.reaction_text[1], 0)
                found_contessa = any(card.card_type == 'Contessa' for card in target.cards)
                response = self.wait_for_any_response(target, self.game)
                if response == self.reaction_text[0]:
                    game.clear_text(self)
                    game.draw_action_text(self, self.reaction_text[0], 0)
                    self.turn_made = True
                elif response == self.reaction_text[2]:
                    game.clear_text(self)
                    game.draw_action_text(self, self.reaction_text[2], -25)
                    if found_contessa:
                        self.remove_random_card(self, game)
                        target.draw_new_card('Contessa', game)
                    elif not found_contessa:
                        if len(target.cards) == 1:
                            target.remove_random_card(target, game)

                        elif len(target.cards) == 2:
                            target.remove_random_card(target, game)
                            target.remove_random_card(target, game)

            self.turn_made = True

    def exchange_cards(self, deck, game): # Works as intended
        game.draw_action_text(self, self.moves[5], -20)
        game.response_order = [p for p in game.players if p != game.current_player and not p.eliminated]
        responder, response = self.accept_or_challenge(game)

        if response == self.reaction_text[0]:
            self.change_card = True
            game.exchange_cards()

        elif response == self.reaction_text[2]:
            self.change_card = False
            game.resolve_challenge(self, responder, 'Ambassador')
            if self.change_card:
                game.exchange_cards()
        self.turn_made = True

    def coup(self, game):
        game.draw_action_text(self, self.moves[6], 0)
        target = game.select_target()
        game.draw_action_text(target, 'TARGET', 0)
        if target and self.coins >= 7:
            self.coins -= 7
            game.game_coins += 7
            self.remove_random_card(target, game.deck)
        self.turn_made = True

    def block(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.block_key:
                return True
        return False

    def accept_or_challenge(self, game):
        responses = {}
        blocking_player = None

        for player in game.response_order:

            response = None
    
            while response is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            response = player.reaction_text[0]
                            offset = 0
                        elif event.key == pygame.K_c:
                            response = player.reaction_text[2]
                            offset = -25

                if response:
                    game.draw_action_text(player, response, offset)
                    responses[player] = response
                    if response == player.reaction_text[2]:
                        blocking_player = player
                        return blocking_player, response
        return None, self.reaction_text[0]

    def player_accept_challenge(self, game):
        response = None
    
        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        response = self.reaction_text[0]
                        offset = 0
                    elif event.key == pygame.K_c:
                        response = self.reaction_text[2]
                        offset = -25

            if response:
                game.draw_action_text(self, response, offset)
                return self, response

    def accept_or_block(self, game):
        
        responses = {}
        blocking_player = None

        for player in game.response_order:

            response = None
    
            while response is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            response = player.reaction_text[0]
                            offset = 0
                        elif event.key == pygame.K_b:
                            response = player.reaction_text[1]
                            offset = 0

                if response:
                    game.draw_action_text(player, response, offset)
                    responses[player] = response
                    if response == player.reaction_text[1]:
                        blocking_player = player
                        return blocking_player, response
        return None, self.reaction_text[0]
    
    def wait_for_any_response(self, player, game):
        
        response = None

        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        response = player.reaction_text[0]
                        offset = 0
                    elif event.key == pygame.K_b:
                        response = player.reaction_text[1]
                        offset = 0
                    elif event.key == pygame.K_c:
                        response = player.reaction_text[2]
                        offset = -25

        if response:
            game.clear_text(player)
            game.draw_action_text(player, response, offset)

        return response

    def has_card(self, card_name):
        for card in self.cards:
            if card.card_type in card_name:
                return card
        return None

    def block_play(self, responder, card_type):

        _, accept = self.player_accept_challenge(self.game)

        if accept == self.reaction_text[0]:
            self.game.clear_text(responder)
            self.game.clear_text(self)
            self.game.draw_action_text(self, self.reaction_text[0], 0)
            self.block = False

        elif accept == self.reaction_text[2]:
   
            self.game.clear_text(responder)
            self.game.clear_text(self)
            self.game.draw_action_text(self, self.reaction_text[2], -25)

            if responder.has_card(card_type):
                responder.player_swap_card(card_type, self.game)
                remove_card = self.cards.pop()
                self.game.deck.removed_deck.append(remove_card)
            else:
                remove_card = responder.cards.pop()
                self.game.deck.removed_deck.append(remove_card)
                self.game.game_coins -= 2
                self.coins += 2
                
        self.turn_made = True

    def player_swap_card(self, card_type, game):
        for card in self.cards:
            if card.card_type == card_type:
                self.cards.remove(card)
                self.game.deck.deck.append(card)
                new_card = self.game.deck.deck.pop()
                self.cards.append(new_card)
                break

    def select_target(self, game):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    target_index = event.key - pygame.K_1
                    if 0 <= target_index < len(game.players):
                        target = game.players[target_index]
                        if target != self and not target.eliminated:
                            return target

            game.render()
            pygame.display.update()
            game.clock.tick(60)

    def remove_random_card(self, player, deck):
        card = random.choice(player.cards)
        self.deck.removed_deck.append(card)
        player.cards.remove(card)
        return

    def draw_new_card(self, card_type, game):  # player has third card
        for card in self.cards:
            if card.card_type == card_type:
                self.cards.remove(card)
                self.game.deck.deck.append(card)
                self.game.deck.shuffle_deck()
                new_card = self.game.deck.deck.pop()
                self.cards.append(new_card)
        return
