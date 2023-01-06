'''
Author: Onur Aslan
Date: 2023-01-05
Objective: coding example 4.1
'''
import numpy as np

class State:
    '''
    Object for states
    '''
    def __init__(self, terminal=None):
        self.terminal = terminal
        if self.terminal:
            self.value = 0
        else:
            self.value = 0 # initialization.  initial value is 0

class Gridworld:
    """
    Gridworld object
    """
    def __init__(self, n_grid = 4):
        self.state_list = [State() for _ in range(n_grid * n_grid)]
        self.state_list[0] = State(terminal=True)
        self.state_list[-1] = State(terminal=True)
        self.state_array = np.array(self.state_list).reshape(n_grid, n_grid)

class Agent:
    """
    Object for agent
    """
    def __init__(self):
        action_prob = 0.25
        self.actions = {'up':action_prob, 'down':action_prob, 'right':action_prob, 'left':action_prob}

if __name__ == "__main__":
    env = Gridworld()
    print(env.state_array[0, 1].value)