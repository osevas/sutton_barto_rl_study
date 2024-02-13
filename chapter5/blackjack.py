'''
Author: Onur Aslan
Date: 2023-11-25
Objective: coding example 5.1, first-visit Monte Carlo prediction for Blackjack
'''
# Libraries
import numpy as np


# Global variables
GAMMA = 1 # discount factor
NUM_EPISODES = 10000000 # number of episodes

class Player:
    """
    Player class for Blackjack
    """
    def __init__(self, current_sum, dealer_card, usable_ace):
        """
        constructor of the class

        Args:
            current_sum (int): current sum of the player
            usable_ace (bool): whether the player has a usable ace
            dealer_card (int): dealer's card
        """
        self.current_sum = current_sum
        self.usable_ace = usable_ace
        self.dealer_card = dealer_card

    def add_card(self, card):
        """
        adds a card to the hand

        Args:
            card (str): card to be added
        """
        if self.usable_ace and self.current_sum + card > 21:
            self.usable_ace = False
            self.current_sum = self.current_sum + card - 10
        else:
            self.current_sum = self.current_sum + card
            

    def get_value(self):
        """
        calculates the value of the hand

        Returns:
            int: value of the hand
        """
        return self.current_sum

class Dealer:
    """
    Dealer class for Blackjack
    """
    def __init__(self, dealer_card):
        """
        constructor of the class

        Args:
            dealer_card (int): dealer's card
        """
        self.dealer_cards = [dealer_card]
    
    def add_card(self):
        """
        adds a card to the hand

        Returns:
            int: card to be added
        """
        self.dealer_cards.append(np.random.randint(1, 11))
    
    def calculate_value(self):
        """
        calculates the value of the hand

        Returns:
            int: value of the hand
        """
        current_sum = 0
        ace_count = 0

        for card in self.dealer_cards:
            if card == 1:
                ace_count += 1
            else:
                current_sum += card
        
        while ace_count > 0:
            ace_count -= 1
            current_sum += 11

            if current_sum > 21:
                current_sum -= 11
                ace_count += 1
                current_sum += ace_count
                break
        
        return current_sum

def init_state():
    """
    initializes the state of the game

    Returns:
        tuple: initial state of the game
    """
    state_value = {}
    state_returns = {}

    for player_sum in range(12, 22):
        for dealer_card in range(1, 11):
            for usable_ace in range(0, 2):
                state_value[(player_sum, dealer_card, usable_ace)] = 0
                state_returns[(player_sum, dealer_card, usable_ace)] = []
    
    return state_value, state_returns

def main():
    """
    main function of the code

    Returns:
        _type_: _description_
    """

    # initialize the state
    state_value, state_returns = init_state()
    

    player_sum = np.random.randint(12, 22)
    dealer_card = np.random.randint(1, 11)
    usable_ace = np.random.randint(0, 2)

    player = Player(player_sum, dealer_card, usable_ace)
    
    
    return None

if __name__ == "__main__":
    main()