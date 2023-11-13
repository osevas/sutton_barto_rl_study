'''
Author: Onur Aslan
Date: 2023-11-11
Objective: coding example 4.2, Jack's Car Rental
'''
import random
import numpy as np
from scipy.stats import poisson

actions = list(range(-5, 6, 1))
MAX_NUM_CARS = 20
MAX_TRANSFER = 5

class Shop:
    """
    object for shops
    """
    def __init__(self, num_cars, prob_rent, prob_return) -> None:
        self.num_cars = num_cars
        self.prob_rent = prob_rent
        self.prob_return = prob_return
        self.max_num_cars = MAX_NUM_CARS
        self.max_transfer = MAX_TRANSFER
    
    def poisson(self) -> list:
        """
        function for Poisson distribution

        Args:
            param_lambda (int): lambda in Poisson's distribution

        Returns:
            int: Poisson probability
        """
        rv = poisson(self.prob_rent)
        x = np.arange(rv.ppf(0.0001), rv.ppf(0.9999))
        rent_probs = [(item, rv.pmf(item)) for item in x] # rent count and its probability from Poisson distribution

        rv = poisson(self.prob_return)
        x = np.arange(rv.ppf(0.0001), rv.ppf(0.9999))
        return_probs = [(item, rv.pmf(item)) for item in x] # return count and its probability from Poisson distribution

        return rent_probs, return_probs

class State:
    """
    object for state
    """
    def __init__(self, num_car_a, a_rent_lambda, a_return_lambda, num_car_b, b_rent_lambda, b_return_lambda) -> None:
        self.shop_a = Shop(num_car_a, a_rent_lambda, a_return_lambda)
        self.shop_b = Shop(num_car_b, b_rent_lambda, b_return_lambda)
        self.val = 0

        # assigning random policy to states
        # narrowing down the actions per car populations in the shops.  if shop_a has 2 cars, then random action will be chosen from narrowed down actions.
        if num_car_a >= MAX_TRANSFER:
            right_end = 100
        elif num_car_a < MAX_TRANSFER:
            right_end = actions.index(num_car_a)
        if num_car_b >= MAX_TRANSFER:
            left_end = 0
        elif num_car_b < MAX_TRANSFER:
            left_end = actions.index(-1 * num_car_b)
        # print(f'Left end: {left_end}, right end: {right_end}')
        # print(f'Narrowed actions: {actions[left_end : right_end + 1]}')
        self.policy = random.choice(actions[left_end : right_end + 1]) 
        # print(self.policy)
        



class Environment:
    """
    object for environment
    """
    def __init__(self, n_grid=MAX_NUM_CARS + 1) -> None:
        self.state_list = []
        for i in range(n_grid):
            for j in range(n_grid):
                self.state_list.append(State(i, 3, 3, j, 4, 2))
        self.state_arr = np.array(self.state_list).reshape(n_grid, n_grid) # shop_a is in rows, shop_b is in columns
        # print(self.state_arr[-1, -1].shop_a.num_cars)
        # print(self.state_arr[-1, -1])
        

class Agent:
    """
    object for agent
    """
    def __init__(self) -> None:
        self.actions = actions

def policy_eval(state_array):
    """
    Policy evaluation in state array

    Args:
        state_array (_type_): _description_

    Returns:
        _type_: _description_
    """
    delta = 0
    # looping over states in Environment.state_arr
    for i in range(state_array.shape[0]):
        for j in range(state_array.shape[1]):
            print(f'# of cars in State {i},{j}: {state_array[i, j].shop_a.num_cars}')

    return None


def main():
    """
    main function of the code

    Returns:
        _type_: _description_
    """

    # Initialization
    # agent1 = Agent()
    env1 = Environment()
    policy_eval(env1.state_arr)
    
    return None

if __name__ == "__main__":
    main()