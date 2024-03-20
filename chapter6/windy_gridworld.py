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
        self.action_val = {'up':0, 'down':0, 'right':0, 'left':0}
        self.loc = [-1, -1]
    
    def update_edges(self, edge: str) -> None:
        """
        updating edges attribute of State object

        """
        self.edges.append(edge)
    
    def update_state_action_val(self, action:str , val:int) -> None:
        """
        updating state value

        Args:
            val (int): new value
        """
        self.action_val[action] = val
    
    def record_loc(self, loc:list) -> None:
        """
        recording location of the state

        Args:
            loc (tuple): location of the state
        """
        self.loc[0] = loc[0]
        self.loc[1] = loc[1]

class Gridworld:
    """
    Gridworld object
    """
    def __init__(self, n_grid_x = 10, n_grid_y = 7):
        self.state_list = [State() for _ in range(n_grid_x * n_grid_y)]
        self.state_array = np.array(self.state_list).reshape(n_grid_y, n_grid_x)
        self.n_grid_x = n_grid_x
        self.n_grid_y = n_grid_y
        self.wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

        # assigning edges to states
        for i in range(n_grid_y): # (0, 0) is the top left corner of the grid
            for j in range(n_grid_x):
                self.state_array[i, j].record_loc((i, j))
                if i == 0 and j == 0:
                    self.state_array[i, j].update_edges('left')
                    self.state_array[i, j].update_edges('up')
                elif i == 0 and j == n_grid_x - 1:
                    self.state_array[i, j].update_edges('right')
                    self.state_array[i, j].update_edges('up')
                elif i == 0:
                    self.state_array[i, j].update_edges('up')
                elif i != 0 and i != n_grid_y - 1:
                    if j == 0:
                        self.state_array[i, j].update_edges('left')
                    if j == n_grid_x - 1:
                        self.state_array[i, j].update_edges('right')
                elif i == n_grid_y - 1 and j == 0:
                    self.state_array[i, j].update_edges('left')
                    self.state_array[i, j].update_edges('down')
                elif i == n_grid_y - 1 and j == n_grid_x - 1:
                    self.state_array[i, j].update_edges('right')
                    self.state_array[i, j].update_edges('down')
                elif i == n_grid_y - 1:
                    self.state_array[i, j].update_edges('down')
        
        # assigning terminal states
        self.state_array[3, 7].terminal = True
    
    def state_to_arr(self) -> np.ndarray:
        """
        Assigning state values to numpy array

        Returns:
            ndarray: current state values in the grid
        """
        current_state_vals = np.zeros((self.n_grid_y, self.n_grid_x))
        for i in range(self.n_grid_y):
            for j in range(self.n_grid_x):
                current_state_vals[i, j] = self.state_array[i, j].value
        return current_state_vals
    
    def arr_to_state(self, arr) -> None:
        """
        Updating state values at the end of the iteration

        Args:
            arr (ndarray): array containing new values
        """
        for i in range(self.n_grid_y):
            for j in range(self.n_grid_x):
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

def e_greedy(state:object, timestep:int) -> str:
    """
    function to select an action

    Args:
        state (object): _description_
        timestep (int): _description_

    Returns:
        str: _description_
    """
    epsilon = 1/timestep
    p = np.random.random()
    if p < epsilon:
        return np.random.choice(list(state.action_val.keys()))
    return max(state.action_val, key = state.action_val.get)

def find_next_state(env:object, current_state:object, action:str, wind:list) -> object:
    """
    function to find the next state

    Args:
        current_state (object): _description_
        action (str): _description_
        wind (list): _description_

    Returns:
        object: _description_
    """
    if action == 'up':
        next_state_loc = [current_state.loc[0] - 1 - wind[current_state.loc[1]], current_state.loc[1]]
    elif action == 'down':
        next_state_loc = [current_state.loc[0] + 1 - wind[current_state.loc[1]], current_state.loc[1]]
    elif action == 'right':
        next_state_loc = [current_state.loc[0] - wind[current_state.loc[1] + 1], current_state.loc[1] + 1]
    elif action == 'left':
        next_state_loc = [current_state.loc[0] - wind[current_state.loc[1] - 1], current_state.loc[1] - 1]
    if next_state_loc[0] < 0:
        next_state_loc[0] = 0
    elif next_state_loc[0] > 6:
        next_state_loc[0] = 6
    if next_state_loc[1] < 0:
        next_state_loc[1] = 0
    elif next_state_loc[1] > 9:
        next_state_loc[1] = 9
    next_state = env.state_array[next_state_loc[0], next_state_loc[1]]
    return next_state


def play(environment:object, alpha:float = 0.001, gamma:int = 1, max_iter:int = 50, reward:int = -1) -> None:
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
    current_state = environment.state_array[3, 0]

    for i in range(max_iter):
        timestep = 1
        while not current_state.terminal:
            
            act1 = e_greedy(current_state, timestep) # action1 of Sarsa -> string
            next_state = find_next_state(environment, current_state, act1, environment.wind) # finding the next state after action1

            
        




if __name__ == "__main__":
    env = Gridworld()
    # agn = Agent()
    # play(env, agn)
    state_space_values = env.state_to_arr()
    print(state_space_values)
    print(env.state_array[0, 4].edges)