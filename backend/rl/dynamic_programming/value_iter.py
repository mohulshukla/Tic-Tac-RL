# Value Iteration over a Basic Tic-Tac-Toe game

# The Bellman Equation: 
# V(s) = max_a [R(s,a) + gamma * sum_{s'} P(s'|s,a) * V(s')]

# The Bellman Equation for Value Iteration: 
# V(s) = R(s) + gamma * sum_{s'} P(s'|s,pi(s)) * V(s')

import numpy as np
from backend.helpers import position_to_coordinates
import random
from backend.rl.single_tic import SingleTic

class ValueIteration:
    def __init__(self):
        self.game = SingleTic()
        self.all_states = self.game.get_all_states()
        self.values = {}
        self.policy = {}

    def game_state_to_grid(self, state_key):
        return [list(row) for row in state_key]
    
    def get_reward(self, state_key, player="X"):
        grid = self.game_state_to_grid(state_key)
        game = SingleTic(grid)
        
        result = game.game_result()

        if result == player:
            return 1.0 # The player won.
        elif result == 'D':
            return 0.0 # The game is a draw.
        elif result is not None:
            return -1.0 # The game is finished, and the player lost.
        else:
            return 0.0 # The game is not finished.
        
    def get_current_player(self, state_key):
        grid = self.game_state_to_grid(state_key)
        x_count = sum(row.count('X') for row in grid)
        o_count = sum(row.count('O') for row in grid)

        if x_count == o_count:
            return 'X'
        elif x_count == o_count + 1:
            return 'O'
        else:
            # This shouldn't happen in a valid game
            raise ValueError(f"Invalid game state: X={x_count}, O={o_count}")
    
    # We can place the current player in any empty cell
    def get_valid_actions(self, state_key):
        grid = self.game_state_to_grid(state_key)
        valid_actions = []
        for i in range(9):
            row, col = position_to_coordinates(i)
            if grid[row][col] is None:
                valid_actions.append(i)
        return valid_actions
    
    def get_next_state(self, state_key, action):
        grid = self.game_state_to_grid(state_key)
        current_player = self.get_current_player(state_key)
        row, col = position_to_coordinates(action)
        grid[row][col] = current_player
        return tuple(tuple(row) for row in grid)
    
    # The main function that runs the value iteration algorithm and returns the optimal policy!
    def run_value_iteration(self, gamma=0.9, theta=1e-6, max_iterations=100):
        print(f"Starting value iteration on {len(self.all_states)} states...")
        
        # Initialize values for all states to 0
        for state in self.all_states:
            self.values[state] = 0.0

        # Run value iteration
        for iteration in range(max_iterations):
            print(f"Iteration {iteration+1}...")
            delta = 0.0 # Tracking maximum change in value across all states
            
            # At each step, we calculate the expected return of each possible action
            # We keep the maximum over each action—this simulates an agent acting optimally at every step. 

            for state_key in self.all_states:
                old_value = self.values[state_key]

                # Check for terminal state
                grid = self.game_state_to_grid(state_key)
                game = SingleTic(grid)
                result = game.game_result()

                if result is not None:
                    self.values[state_key] = self.get_reward(state_key, player="X")

                # For non-terminal states, calculate the expected return
                else:
                    valid_actions = self.get_valid_actions(state_key)
                    current_player = self.get_current_player(state_key)

                    action_values = []
                    for action in valid_actions:
                        next_state = self.get_next_state(state_key, action)
                        future_value = self.values[next_state]
                        total_value = self.get_reward(state_key, player='X') + gamma * future_value

                        action_values.append(total_value)

                    if current_player == 'X':
                        best_value = max(action_values)
                    else: # From Os perspective, we want to minimize the value (do the most harm to X)
                        best_value = min(action_values)
                    
                    # Update the value for the current state
                    self.values[state_key] = best_value

                # Update delta
                delta = max(delta, abs(self.values[state_key] - old_value))
            
            print(f"Iteration {iteration+1}, max change: {delta:.6f}")

            if delta < theta:
                print(f"Converged after {iteration+1} iterations")
                break
        # Finally, extract the policy
        print("Extracting policy...")
        self._extract_policy(gamma)
        return self.policy


    def _extract_policy(self, gamma=0.9):
        for state_key in self.all_states:
            grid = self.game_state_to_grid(state_key)
            game = SingleTic(grid)
            
            # Skip terminal states (no actions needed)
            if game.game_result() is not None:
                continue
            
            current_player = self.get_current_player(state_key)
            valid_actions = self.get_valid_actions(state_key)
            
            if valid_actions:
                action_values = []
                for action in valid_actions:
                    next_state = self.get_next_state(state_key, action)
                    future_value = self.values[next_state]
                    total_value = gamma * future_value
                    action_values.append((action, total_value))
                
                # Choose best action based on player
                if current_player == 'X':
                    best_action, _ = max(action_values, key=lambda x: x[1])
                else:
                    best_action, _ = min(action_values, key=lambda x: x[1])
                
                self.policy[state_key] = best_action
        
        print(f"Policy extracted for {len(self.policy)} non-terminal states")

        


def test_custom():
    vi = ValueIteration()
    policy = vi.run_value_iteration()

    # Create any test state
    test_grid = [['X', 'X', 'O'], 
                [None, 'O', 'X'], 
                ['O', 'O', 'X']]
    test_state = tuple(tuple(row) for row in test_grid)

    current_player = vi.get_current_player(test_state)

    print(f"Optimal move for {current_player}: {policy[test_state]}")


def main():
    vi = ValueIteration()
    policy = vi.run_value_iteration()
    SingleTic.simulate_game(policy)
    


if __name__ == "__main__":
    main()