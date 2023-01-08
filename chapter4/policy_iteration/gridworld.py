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
    def __init__(self, terminal=None) -> None:
        self.terminal = terminal
        if self.terminal:
            self.value = 0
        else:
            self.value = 0 # initialization.  initial value is 0
        self.edges = []
    
    def update_edges(self, edge: str) -> None:
        """
        updating edges attribute of State object

        """
        self.edges.append(edge)

class Gridworld:
    """
    Gridworld object
    """
    def __init__(self, n_grid = 4):
        self.state_list = [State() for _ in range(n_grid * n_grid)]
        self.state_list[0] = State(terminal=True)
        self.state_list[-1] = State(terminal=True)
        self.state_array = np.array(self.state_list).reshape(n_grid, n_grid)

        # assigning edges to states
        for i in range(n_grid):
            for j in range(n_grid):
                if i == 0 and j == 0:
                    self.state_array[i, j].update_edges('left')
                    self.state_array[i, j].update_edges('up')
                elif i == 0 and j == n_grid - 1:
                    self.state_array[i, j].update_edges('right')
                    self.state_array[i, j].update_edges('up')
                elif i == 0:
                    self.state_array[i, j].update_edges('up')
                elif i != 0 and i != n_grid - 1:
                    if j == 0:
                        self.state_array[i, j].update_edges('left')
                    if j == n_grid - 1:
                        self.state_array[i, j].update_edges('right')
                elif i == n_grid - 1 and j == 0:
                    self.state_array[i, j].update_edges('left')
                    self.state_array[i, j].update_edges('down')
                elif i == n_grid - 1 and j == n_grid - 1:
                    self.state_array[i, j].update_edges('right')
                    self.state_array[i, j].update_edges('down')
                elif i == n_grid - 1:
                    self.state_array[i, j].update_edges('down')


class Agent:
    """
    Object for agent
    """
    def __init__(self):
        self.action_prob = 0.25
    
    def move(self) -> dict:
        """
        Possible moves of an agent
        """
        actions = {'up':self.action_prob, 'down':self.action_prob, 'right':self.action_prob, 'left':self.action_prob}
        return actions

if __name__ == "__main__":
    env = Gridworld()
    print(env.state_array[3, 0].value)
    print(env.state_array[3, 3].edges)