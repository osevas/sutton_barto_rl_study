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
RENT_REWARD = 10
TRANSFER_REWARD = -2
GAMMA = 0.9
THETA = 

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

def calc_sigma(rent_a, state_array, rent_b, return_a, return_b, i, j):
    """
    calculating summation
    """
    if (rent_a[0] <= state_array[i, j].shop_a.num_cars) and (rent_b[0] <= state_array[i, j].shop_b.num_cars): 
        # rentable car count should be less or equal to current car count in the shop
        
        # calculating shop's new car counts
        if state_array[i, j].policy < 0:
            # shop_b is transferring cars to shop_a
            new_shop_a_num_car = state_array[i, j].shop_a.num_cars - rent_a[0] + return_a[0] + abs(state_array[i, j].policy)
            new_shop_b_num_car = state_array[i, j].shop_b.num_cars - rent_b[0] + return_b[0] - abs(state_array[i, j].policy)
        
        elif state_array[i, j].policy > 0:
            # shop_b is transferring cars to shop_a
            new_shop_a_num_car = state_array[i, j].shop_a.num_cars - rent_a[0] + return_a[0] - abs(state_array[i, j].policy)
            new_shop_b_num_car = state_array[i, j].shop_b.num_cars - rent_b[0] + return_b[0] + abs(state_array[i, j].policy)
        
        # checking if new car counts are within the limits
        if (new_shop_a_num_car > 0) and (new_shop_b_num_car > 0):
            # calculating probability of the state
            total_prob = rent_a[1] * return_a[1] * rent_b[1] * return_b[1]

            # calculating reward
            reward = (rent_a[0] + rent_b[0]) * RENT_REWARD + state_array[i, j].policy * TRANSFER_REWARD

            state_new_value += total_prob * (reward + GAMMA * state_array[new_shop_a_num_car, new_shop_b_num_car].val)
    return state_new_value

def policy_eval(state_array):
    """
    Policy evaluation in state array

    Args:
        state_array (_type_): _description_

    Returns:
        _type_: _description_
    """
    delta = 0

    while delta < THETA:
        # looping over states in Environment.state_arr
        for i in range(state_array.shape[0]):
            for j in range(state_array.shape[1]):
                # print(f'# of cars in State {i},{j}: {state_array[i, j].shop_a.num_cars}')
                state_value_temp = state_array[i, j].val # recording initial state value

                rent_prob_a, return_prob_a = state_array[i, j].shop_a.poisson()
                rent_prob_b, return_prob_b = state_array[i, j].shop_b.poisson()

                state_new_value = 0
                # Looping over rent and return probabilities for shop_a and shop_b
                for rent_a in rent_prob_a: # rent_a and rent_b are tuples -> (rent count, rent probability)
                    for return_a in return_prob_a:
                        for rent_b in rent_prob_b:
                            for return_b in return_prob_b:
                                # print(f'Rent prob: {rent_a[1]}, Return prob: {return_a[1]}')
                                # print(f'Rent prob: {rent_b[1]}, Return prob: {return_b[1]}')
                                # print(f'Policy: {state_array[i, j].policy}')
                                # print(f'Value: {state_array[i, j].val}')
                                state_new_value = calc_sigma(rent_a, state_array, rent_b, return_a, return_b, i, j)
                                
                state_array[i, j].val = state_new_value
                delta = max(delta, abs(state_value_temp - state_array[i, j].val))
                print(f'Delta: {delta}')




        break


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