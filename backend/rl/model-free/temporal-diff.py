import numpy as np
from backend.helpers import position_to_coordinates
import random
from backend.rl.single_tic import SingleTic


# Temporal Difference Learning for Tic-Tac-Toe. Using the Q Learning method
class TemporalDifference:
    def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.game = SingleTic()
        self._initialize_Q_values()
        self.episode_count = 0
        
        # Hyperparameters
        self.epsilon = epsilon
        self.alpha = alpha  
        self.gamma = gamma

    def _initialize_Q_values(self):
        self.Q = {}


    def q_learning_update():

    def get_action(self, state_key):
        valid_actions = self.game.get_valid_actions(state_key)
        if random.random() < self.epsilon: # this is the exploration scenario
            return random.choice(valid_actions)
        else:
            # Get the best action for the current state, and player (act greedily)
            q_values = []
            for action in valid_actions:
                q_value = self._get_Q_value(state_key, action)
                q_values.append(q_value)
            
            current_player = self.game.get_current_player(state_key)

            if current_player == 'X':
                best_action = valid_actions[np.argmax(q_values)]
            else:
                best_action = valid_actions[np.argmin(q_values)]

            return best_action
        

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