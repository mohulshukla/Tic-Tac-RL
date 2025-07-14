import numpy as np
from backend.helpers import position_to_coordinates
import random
from backend.rl.single_tic import SingleTic


# Monte Carlo Method for Tic-Tac-Toe
class MonteCarlo:
    def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.game = SingleTic()
        self._initialize_Q_values()
        self.policy = {}  # Current policy
        self.episode_history = []
        self.episode_count = 0
        
        # Hyperparameters
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha      # Learning rate  
        self.gamma = gamma      # Discount factor


        
    
    def _initialize_Q_values(self):
        # Let's initialize an empty Q table, which we will populate as we encounter episodes.
        self.Q = {} # Q(s,a) values - our main learning target
        self.returns = {}  # For storing returns for each (s,a) pair
    
    
    def generate_episode(self):
        episode = []
        game = SingleTic() # A fresh new game

        while not game.game_result():
            state_key = game.get_state_key()
            valid_actions = game.get_valid_actions(state_key)

            if random.random() < self.epsilon:
                action = random.choice(valid_actions)

    
    def get_action(self, state_key):
        valid_actions = self.game.get_valid_actions(state_key)
        if random.random() < self.epsilon: # this is the 
            return random.choice(valid_actions)
        else:
            return self.policy[state_key]
        
   

    def _get_Q_value(self, state_key, action):
        if state_key not in self.Q:
            self.Q[state_key] = {}
            for action in self.game.get_valid_actions(state_key):
                self.Q[state_key][action] = 0.0
        return self.Q[state_key][action]
    
    def _set_Q_value(self, state_key, action, value):
        if state_key not in self.Q:
            self.Q[state_key] = {}
        self.Q[state_key][action] = value

    


 

