'''
Author: Onur Aslan
Date: 2023-11-25
Objective: coding example 5.1, Blackjack
'''
class Player:
    """
    Player class for Blackjack
    """
    def __init__(self, name, hand):
        """
        constructor of the class

        Args:
            name (str): name of the player
            hand (list): list of cards in hand
        """
        self.name = name
        self.hand = hand

    def __str__(self):
        """
        string representation of the class

        Returns:
            str: string representation of the class
        """
        return "Player " + self.name + " has " + str(self.hand)

    def add_card(self, card):
        """
        adds a card to the hand

        Args:
            card (str): card to be added
        """
        self.hand.append(card)

    def get_value(self):
        """
        calculates the value of the hand

        Returns:
            int: value of the hand
        """
        value = 0
        ace = False
        for card in self.hand:
            if card[0] in "JQK":
                value += 10
            elif card[0] == "A":
                ace = True
                value += 1
            else:
                value += int(card[0])
        if ace and value + 10 <= 21:
            value += 10
        return value

def main():
    """
    main function of the code

    Returns:
        _type_: _description_
    """

    
    
    
    return None

if __name__ == "__main__":
    main()