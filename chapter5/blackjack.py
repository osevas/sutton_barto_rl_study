'''
Author: Onur Aslan
Date: 2023-11-25
Objective: coding example 5.1, first-visit Monte Carlo prediction for Blackjack
'''
# Libraries
import numpy as np
import matplotlib.pyplot as plt


# Global variables
GAMMA = 1 # discount factor
NUM_EPISODES = 500000 # number of episodes

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
    
    for episode in range(NUM_EPISODES):
        print(f"Episode: {episode}")
        # initialize the player and the dealer
        track_states = []
        player_sum = np.random.randint(12, 22)
        dealer_card = np.random.randint(1, 11)
        usable_ace = np.random.randint(0, 2)
        track_states.append((player_sum, dealer_card, usable_ace))

        player = Player(player_sum, dealer_card, usable_ace)
        dealer = Dealer(dealer_card)

        while player.get_value() <= 21:
            if player.get_value() == 21:
                will_hit = False
            else:
                will_hit = np.random.choice([True, False])

            if will_hit:
                player.add_card(np.random.randint(1, 11))
                player_sum = player.get_value()
                for state in state_value:
                    if state == (player_sum, dealer_card, usable_ace):
                        track_states.append((player_sum, dealer_card, usable_ace))
                if player_sum > 21:
                    reward = -1
                    num_states = len(track_states)
                    for state in track_states:
                        state_value[state] = state_value[state] + reward / num_states
                    print(f"Player sum: {player_sum}, Dealer card: {dealer.calculate_value()}, Usable ace: {usable_ace}, Reward: {reward}")
                    break # exit while loop
            
            elif not will_hit: # dealer's turn since player has sticked
                dealer_sum = dealer.calculate_value()
                while dealer_sum < 17:
                    dealer.add_card()
                    dealer_sum = dealer.calculate_value()
                    for state in state_value:
                        if state == (player_sum, dealer_sum, usable_ace):
                            track_states.append((player_sum, dealer_sum, usable_ace))
                
                if dealer_sum > 21 or player_sum > dealer_sum:
                    reward = 1
                elif player_sum == dealer_sum:
                    reward = 0
                elif player_sum < dealer_sum:
                    reward = -1

                num_states = len(track_states)
                for state in track_states:
                    state_value[state] = state_value[state] + reward / num_states
                
                break # exit while loop
    
    return state_value

def plot_value_function(state_value: dict):
    """
    plots the value function
    """
    len_state_value = len(state_value)
    usable_ace = np.zeros((int(len_state_value / 2), 3))
    no_usable_ace = np.zeros((int(len_state_value / 2), 3))

    i, j = 0, 0
    for key, value in state_value.items():
        if key[2] == 0: # no usable ace
            no_usable_ace[i, 0] = key[0]
            no_usable_ace[i, 1] = key[1]
            no_usable_ace[i, 2] = value
            i += 1
        elif key[2] == 1: # usable ace
            usable_ace[j, 0] = key[0]
            usable_ace[j, 1] = key[1]
            usable_ace[j, 2] = value
            j += 1
        
    
    fig = plt.figure()
    ax = fig.add_subplot(121, projection='3d')
    ax.scatter(usable_ace[:, 0], usable_ace[:, 1], usable_ace[:, 2], c='r', marker='o', )
    ax.set_xlabel('Player Sum')
    ax.set_ylabel('Dealer Card')
    ax.set_zlabel('Value')
    ax.set_title('Usable Ace')

    ax = fig.add_subplot(122, projection='3d')
    ax.scatter(no_usable_ace[:, 0], no_usable_ace[:, 1], no_usable_ace[:, 2], c='b', marker='o')
    ax.set_xlabel('Player Sum')
    ax.set_ylabel('Dealer Card')
    ax.set_zlabel('Value')
    ax.set_title('No Usable Ace')

    plt.show()
    return None

if __name__ == "__main__":
    state_value = main()
    plot_value_function(state_value)
    print(len(state_value))