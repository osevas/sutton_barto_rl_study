'''
Author: Onur Aslan
Date: 2024-03-23
Objective: coding example 6.5. Windy Gridworld with Sarsa
'''
import numpy as np
np.set_printoptions(precision=3, linewidth=500)

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
                current_state_vals[i, j] = self.state_array[i, j].action_val[max(self.state_array[i, j].action_val, key=self.state_array[i, j].action_val.get)] # max value of the state
        return current_state_vals
    
    def env_directions(self) -> np.ndarray:
        """
        Showing directions with max values of the states

        Returns:
            ndarray: current state actions in the grid with max values
        """
        current_state_dirs = np.chararray((self.n_grid_y, self.n_grid_x), itemsize = 5)
        for i in range(self.n_grid_y):
            for j in range(self.n_grid_x):
                current_state_dirs[i, j] = max(self.state_array[i, j].action_val, key=self.state_array[i, j].action_val.get) # max value of the state
        return current_state_dirs
    
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
    # epsilon = 1/timestep
    epsilon = 0.1
    p = np.random.random()
    if p < epsilon:
        return np.random.choice(list(state.action_val.keys()))
    return max(state.action_val, key = state.action_val.get) # returns the action in string format

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
        next_state_loc = [current_state.loc[0] - wind[current_state.loc[1]], current_state.loc[1] + 1]
    elif action == 'left':
        next_state_loc = [current_state.loc[0] - wind[current_state.loc[1]], current_state.loc[1] - 1]
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


def play(environment:object, alpha:float = 0.5, gamma:int = 1, max_iter:int = 700, reward:int = -1) -> None:
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
    
    for episode in range(max_iter):
        current_state = environment.state_array[3, 0]
        timestep = 1
        while not current_state.terminal:
            
            act1 = e_greedy(current_state, timestep) # action1 of Sarsa -> string
            next_state = find_next_state(environment, current_state, act1, environment.wind) # finding the next state after action1

            act2 = e_greedy(next_state, timestep) # action2 of Sarsa -> string

            # updating the value of the current state
            current_state.update_state_action_val(act1, current_state.action_val[act1] + alpha*(reward + gamma*next_state.action_val[act2] - current_state.action_val[act1]))
            current_state = next_state
            timestep += 1
        print('Episode: ', episode + 1, ' is completed with ', timestep, ' timesteps')
    print('Training is completed')
    print(environment.env_directions())
    print('\n')
    print(environment.state_to_arr())
    
    return None


if __name__ == "__main__":
    env = Gridworld()
    
    # state_space_values = env.state_to_arr()
    # print(state_space_values)
    # print(env.state_array[0, 4].edges)
    
    play(env)
    