import numpy as np
import random


class BlackJackActions:
    '''
    
    Black Jack Actions class and Random action sampler
    Actions
        1 : Hit
        0 : Stick
        
    '''
    def __init__(self):
        self.action_space = np.array([1, 0])
        
    def sample(self):
        return np.random.choice(self.action_space)


class BlackJackStylised:
    '''
    Deck Setup
        Card Suits : Spades, Hearts, Diamonds and Clubs
        Face Cards : Kings, Queens and Jacks
        Ace = Aces
        Number cards : 2 to 10
        
    Card value setup
        Face cards : 10
        Ace : 11 if bust 1
        Number : Numerical value equal to their number
        
        
    Actions
        1 : Hit
        0 : Stick
    '''
    
    _card_suits = ['S', 'H', 'D', 'C']
    _face_cards = ['K', 'Q', 'J']
    _ace = ['A']
    _number_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10'] 
    _face_cards_value = 10
    _usable_ace = 11
    _unusable_ace = 1
    _max_hand_value = 21

    _suitless_group = _ace + _face_cards + _number_cards
    
    def __init__(self, num_decks=None, max_episodes=None):
    
        self.num_decks = num_decks
        self.max_episodes = max_episodes
        self.inf_deck = False
        self.deck_complete = False
        # self.reset_init(hard=True)
        
    
    def reset_init(self, hard=False):
        '''
        TODO 
        ***Handle Natural black jack while dealing***
        returns Tuple(cards in hand, total sum, useable ace bool, hand complete bool)
        '''
        
        if self.num_decks is None or hard == True:
            self.action = BlackJackActions()
            self._create_n_decks()
            self.episode_counter = 0
            self.hand_complete = False
            self.usable_ace = False
            self.deck_complete = False
        
        else:
            self.hand_complete = False
            self.usable_ace = False
            
        if self.num_decks is None:
            self.player_hand = self._infinitsampler(init = False) #True
        else:
            if self.deck_complete:
                self.hand_complete = True
                # self.current_sum = sum(self.get_card_value(self.player_hand))
                self.current_sum = self.get_card_value(self.player_hand)
                return (self.player_hand, self.current_sum, self.usable_ace, self.hand_complete)
                
            self.player_hand = self._finitsampler(init = False) #True
            
        
        self.current_sum = self.get_card_value(self.player_hand)
        
        if self.current_sum == self._max_hand_value:
            self.hand_complete = True
            print("That's a natural black jack")
                
        return (self.player_hand, self.current_sum, self.usable_ace, self.hand_complete)
        
        
    def step(self, action):
        '''
        returns Tuple(cards in hand, total sum, useable ace bool, hand complete bool)
        '''
        
        if self.hand_complete == True:
            raise Exception('Hand is complete, reset before drawing a card!')
            
        if self.max_episodes is not None:
            if self.episode_counter > self.max_episodes:
                raise Exception('Episode count exceeded maximum limit! Please reset before starting the game.')

            if self.max_episodes is not None:
                self.episode_counter += 1
                    
        # Infinite sampler for infinite decks
        if self.inf_deck: 
            if action == 1:
                self.player_hand.append(self._infinitsampler(init=False)[0])
                self.current_sum = self.get_card_value(self.player_hand)

                if self.current_sum > self._max_hand_value:
                    self.hand_complete = True
                    print('Player is bust total sum is greater than 21!')
                return (self.player_hand, self.current_sum, self.usable_ace, self.hand_complete)
            else:
                self.hand_complete = True
                return (self.player_hand, self.current_sum, self.usable_ace, self.hand_complete)
        
        # TODO WIP  Finite sampler for finite deck 
        else:
            
            if self.deck_complete:
                self.hand_complete = True
                return (self.player_hand, self.current_sum, self.usable_ace, self.hand_complete)

            if action == 1:
                card_drawn = self._finitsampler(init=False)[0]
                
                if self.deck_complete:
                    self.hand_complete = True
                    return (self.player_hand, self.current_sum, self.usable_ace, self.hand_complete)
                    
                self.player_hand.append(card_drawn)
                self.current_sum = self.get_card_value(self.player_hand)

                if self.current_sum > self._max_hand_value:
                    self.hand_complete = True
                    print('Player is bust total sum is greater than 21!')
                return (self.player_hand, self.current_sum, self.usable_ace, self.hand_complete)
            else:
                self.hand_complete = True
                return (self.player_hand, self.current_sum, self.usable_ace, self.hand_complete)
            
        
    
    def _infinitsampler(self, init = False):
        '''
        TODO
        return with a bool of usable_ace
        '''
        if init == True:
            return random.choices(self.decks, k=2)
        else:
            return random.choices(self.decks, k=1)
        
    def _finitsampler(self, init=False):
        
        if init == True:
            if len(self.decks) < 2:
                self.deck_complete = True
                return []
            
            cards_dealt = self.decks[-2:]
            self.decks =  self.decks[:-2]
            
            self.card_counter[self._get_suitless_card(cards_dealt[0])]['curr_count'] -= 1
            self.card_counter[self._get_suitless_card(cards_dealt[1])]['curr_count'] -= 1
            
            return cards_dealt
        else:
            if len(self.decks) < 1:
                self.deck_complete = True
                return []
            
            card_drawn = self.decks.pop()
            self.card_counter[self._get_suitless_card(card_drawn)]['curr_count'] -= 1
            return [card_drawn]
        
    def _get_suitless_card(self, suit_card):
        return suit_card.split('.')[-1]
        
    def _create_deck(self):
        
        deck = []
        for suit in self._card_suits:
            for suitless_card in self._suitless_group:
                deck.append(suit+'.'+suitless_card)
                
        np.random.shuffle(deck)
        
        return deck
        
    def _create_n_decks(self):
        
        if self.num_decks is None:
            self.decks = self._create_deck()
            self.inf_deck = True
            
        else:
            self.decks = []
            self._create_card_counter()
            
            for i in range(self.num_decks):
                self.decks += self._create_deck()
            
            np.random.shuffle(self.decks)
            
    def _create_card_counter(self):
        
        card_keys = self._face_cards + self._ace + self._number_cards
        self.card_counter = {}
        for key in card_keys:
            self.card_counter[key] = {'curr_count':self.num_decks*4, 'total':self.num_decks*4}
                    
        

    def get_card_value(self, cards):
        '''
        Returns list of card values individually
        '''
        
        non_ace_hand_values = []
        ace_count = 0
        num_usable_aces = 0
        
        for card in cards:
            suitless_card = card.split('.')[-1]

            if suitless_card in self._number_cards:
                non_ace_hand_values.append(int(suitless_card))

            elif suitless_card == 'A':
                ace_count += 1
            else:
                non_ace_hand_values.append(self._face_cards_value)
                
        non_ace_curr_sum = sum(non_ace_hand_values)
        # print(f'DEBUG : non_ace_curr_sum : {non_ace_curr_sum}')
    
        if ace_count > 0:
            num_usable_aces = self._ace_accomodation(non_ace_curr_sum)
            if num_usable_aces > 0:
                self.usable_ace = True
            else:
                self.usable_ace = False
        else:
             self.usable_ace = False
                
        return non_ace_curr_sum + num_usable_aces*self._usable_ace + (ace_count-num_usable_aces)

        
    def _ace_accomodation(self, non_ace_curr_sum):
        check_val = np.floor((self._max_hand_value - non_ace_curr_sum)/self._usable_ace)
        if check_val < 0:
            return 0
        return check_val
        # return curr_sum
        