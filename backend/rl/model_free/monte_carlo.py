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
        self.Q = {} # Q(s,a) values - our main learning target. this is from X's perspective!
        self.returns = {}  # For storing returns for each (s,a) pair
    
    
    def train(self, num_episodes=100000, verbose=True):

        x_wins, o_wins, draws = 0, 0, 0
        for episode_count in range(num_episodes):
            episode, final_reward = self.generate_episode()
            self.update_Q_values(episode, final_reward)

            
            if final_reward == 1:
                x_wins += 1
            elif final_reward == -1:
                o_wins += 1
            else:
                draws += 1
            
            self.episode_history.append(episode)
            self.episode_count += 1

            
            if (episode_count + 1) % 1000 == 0 and verbose:
                total = episode_count + 1
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
            
    
    def generate_episode(self):
        episode = []
        game = SingleTic() # A fresh new game

        while not game.game_result():
            state_key = game.get_state_key()

            current_player = game.get_current_player(state_key)
            action = self.get_action(state_key)

            # make the move
            game.make_move(action, current_player)
            episode.append((state_key, action, current_player))
        
        # Assign reward based on final outcome
        final_reward = self._get_final_reward(game, episode)
        return episode, final_reward
    
    def update_Q_values(self, episode, final_reward):
        """Update Q-values using returns from the episode"""
        
        # Calculate returns for each step (working backwards)
        returns = []
        G = 0  # Return starts at 0 and works backward
        
         # Work backwards through episode to calculate discounted returns
        for i in reversed(range(len(episode))):
            state_key, action, player = episode[i]
            
            # For the last step, G = final_reward 
            # For earlier steps, G = gamma * G (discounted future return)
            if i == len(episode) - 1:
                # Final reward, adjusted for player perspective
                G = final_reward 
            else:
                G = self.gamma * G
            
            returns.insert(0, G)  # Insert at beginning to maintain order
        
        # Update Q-values using the calculated returns
        for i, (state_key, action, player) in enumerate(episode):
            # Get current Q-value
            current_q = self._get_Q_value(state_key, action)
            
            # Update using incremental average: Q = Q + α[G - Q]
            new_q = current_q + self.alpha * (returns[i] - current_q)
            self._set_Q_value(state_key, action, new_q)



    def _get_final_reward(self, game, episode):
        # Get the final reward based on the game result
        result = game.game_result()
        if result == 'X':
            return 1
        elif result == 'O':
            return -1
        else:
            return 0

    
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
    mc = MonteCarlo()
    policy = mc.train()
    SingleTic.simulate_game(policy)


if __name__ == "__main__":
    main()