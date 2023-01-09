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
    def __init__(self, terminal:bool = False) -> None:
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
    
    def update_val(self, val:int) -> None:
        """
        updating state value

        Args:
            val (int): new value
        """
        self.value = val

class Gridworld:
    """
    Gridworld object
    """
    def __init__(self, n_grid = 4):
        self.state_list = [State() for _ in range(n_grid * n_grid)]
        self.state_list[0] = State(terminal=True)
        self.state_list[-1] = State(terminal=True)
        self.state_array = np.array(self.state_list).reshape(n_grid, n_grid)
        self.n_grid = n_grid

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
    
    def state_to_arr(self) -> np.ndarray:
        """
        Assigning state values to numpy array

        Returns:
            ndarray: current state values in the grid
        """
        current_state_vals = np.zeros((self.n_grid, self.n_grid))
        for i in range(self.n_grid):
            for j in range(self.n_grid):
                current_state_vals[i, j] = self.state_array[i, j].value
        return current_state_vals
    
    def arr_to_state(self, arr) -> None:
        """
        Updating state values at the end of the iteration

        Args:
            arr (ndarray): array containing new values
        """
        for i in range(self.n_grid):
            for j in range(self.n_grid):
                self.state_array[i, j].update_val(arr[i, j])




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

def play(environment:object, agent:object, theta:float = 0.001, gamma:int = 1, max_iter:int = 50, reward:int = -1) -> None:
    """
    function to start an iteration

    Args:
        environment (object): _description_
        agent (object): _description_
        theta (float, optional): _description_. Defaults to 0.001.
        gamma (int, optional): _description_. Defaults to 1.
        max_iter (int, optional): _description_. Defaults to 50.
        reward (int, optional): _description_. Defaults to -1.
    """
    new_state_arr = np.zeros((environment.n_grid, environment.n_grid))
    num_iter = 1
    delta = 1

    while(delta > theta and num_iter <= max_iter):

        for i in range(environment.n_grid):
            for j in range(environment.n_grid): # going through the grid
                if not environment.state_array[i, j].terminal: # work on states that are not terminal
                    allowable_actions = agent.move() # list allowable actions of the agent
                    new_value = 0
                    for action in allowable_actions.keys():
                        if action in environment.state_array[i, j].edges: # checking if we hit edge wall or not.  if we hit, use state's current value
                            value_action = allowable_actions[action] * (reward + gamma * environment.state_array[i, j].value)
                            new_value += value_action
                        else: # if we do not hit a wall
                            if action == 'up':
                                value_action = allowable_actions[action] * (reward + gamma * environment.state_array[i-1, j].value)
                                new_value += value_action
                            elif action == 'down':
                                value_action = allowable_actions[action] * (reward + gamma * environment.state_array[i+1, j].value)
                                new_value += value_action
                            elif action == 'right':
                                value_action = allowable_actions[action] * (reward + gamma * environment.state_array[i, j+1].value)
                                new_value += value_action
                            elif action == 'left':
                                value_action = allowable_actions[action] * (reward + gamma * environment.state_array[i, j-1].value)
                                new_value += value_action
                    new_state_arr[i, j] = new_value
        
        # calculating delta
        current_state_arr = environment.state_to_arr()
        delta = np.amax(np.absolute(current_state_arr - new_state_arr))

        print('\nCurrent iteration: {}'.format(num_iter))
        print('\nCurrent state values:')
        print(current_state_arr)

        print('\nDelta: {}'.format(delta))

        # updating state values
        environment.arr_to_state(new_state_arr)

        num_iter += 1



if __name__ == "__main__":
    env = Gridworld()
    agn = Agent()
    play(env, agn)