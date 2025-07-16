import numpy as np
from backend.helpers import position_to_coordinates
import random
from backend.rl.single_tic import SingleTic


# Temporal Difference Learning for Tic-Tac-Toe. Using the Q Learning method
class TemporalDifference:
    def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.game = SingleTic()
        self._initialize_Q_values()
        
        # Hyperparameters
        self.epsilon = epsilon
        self.alpha = alpha  
        self.gamma = gamma
        self.policy = {}

    def _initialize_Q_values(self):
        self.Q = {}


    def q_learning_update(self, state_key, action, reward, next_state_key):
        # Q(s,a) = Q(s,a) + alpha * (reward + gamma * max_a' Q(s',a') - Q(s,a))
        current_q_value = self._get_Q_value(state_key, action)
        
        if next_state_key is None:  # Terminal state - game ended
            td_target = reward
        else:
            # Get max Q-value for next state
            valid_actions = self.game.get_valid_actions(next_state_key)
            max_next_q = max(self._get_Q_value(next_state_key, a) for a in valid_actions)
            td_target = reward + self.gamma * max_next_q
        
        new_q_value = current_q_value + self.alpha * (td_target - current_q_value)
        self._set_Q_value(state_key, action, new_q_value)

    def train_episode(self):
        new_game = SingleTic()
        
        while new_game.game_result() is None:
            state_key = new_game.get_state_key()
            current_player = new_game.get_current_player(state_key)
            action = self.get_action(state_key)
            
            # Make the move
            new_game.make_move(action, current_player)
            
            # Handle reward correctly
            if new_game.game_result() is not None:
                # Terminal state: give actual reward
                reward = self.get_reward(new_game.get_state_key())
                self.q_learning_update(state_key, action, reward, None)
            else:
                # Non-terminal state: NO immediate reward
                next_state_key = new_game.get_state_key()
                self.q_learning_update(state_key, action, 0.0, next_state_key)  
        
        return new_game.game_result()

    def get_reward(self, state_key):
        game = SingleTic(self.game.game_state_to_grid(state_key))
        result = game.game_result()

        if result == 'X':
            return 1.0
        elif result == 'O':
            return -1.0
        elif result == 'D':
            return 0.0
        else:
            return 0.0
    
    def train_full(self, iterations=100000):
        x_wins, o_wins, draws = 0, 0, 0
        for i in range(iterations):
            game_result = self.train_episode()
            
            # For logging
            if game_result == 'X':
                x_wins += 1
            elif game_result == 'O':
                o_wins += 1
            else:
                draws += 1
            
            # Print progress every 1k episodes
            if (i + 1) % 1000 == 0:
                total = i + 1
                print(f"Episode {total}: X:{x_wins/total:.2%} O:{o_wins/total:.2%} D:{draws/total:.2%}")
       
        self.extract_policy()
        return self.policy

    def extract_policy(self):
        for state_key in self.Q:
            if state_key not in self.policy:
                valid_actions = self.game.get_valid_actions(state_key)
                current_player = self.game.get_current_player(state_key)
                
                # Get Q-values for all valid actions
                q_values = [self._get_Q_value(state_key, action) for action in valid_actions]
                
                # Choose best action based on player
                if current_player == 'X':
                    best_idx = np.argmax(q_values)
                else:
                    best_idx = np.argmin(q_values)
                
                self.policy[state_key] = valid_actions[best_idx]


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



def main():
    td = TemporalDifference()
    policy = td.train_full()
    SingleTic.simulate_game(policy)

if __name__ == "__main__":
    main()