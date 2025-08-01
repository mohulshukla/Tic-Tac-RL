# Policy Iteration over a Basic Tic-Tac-Toe game

# The Bellman Equation: 
# V(s) = max_a [R(s,a) + gamma * sum_{s'} P(s'|s,a) * V(s')]

# The Bellman Equation for Policy Iteration: 
# V(s) = R(s) + gamma * sum_{s'} P(s'|s,pi(s)) * V(s')


import numpy as np
from backend.helpers import position_to_coordinates
import random
from backend.rl.single_tic import SingleTic

class PolicyIteration:
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
    

    def initialize_policy(self):
        print("Initializing policy randomly...")


        for state_key in self.all_states:
            grid = self.game_state_to_grid(state_key)
            game = SingleTic(grid)

            if game.game_result() is None:
                valid_actions = self.get_valid_actions(state_key)
                self.policy[state_key] = random.choice(valid_actions)

            else:
                self.policy[state_key] = None # Terminal states have no policy

        print(f"Initialized policy for {len(self.policy)} non-terminal states")
        return self.policy
    
    def policy_evaluation(self, gamma=0.9, theta=1e-6, max_iterations=20):
        print("=== EVALUATING POLICY ===")

        # Initialize values for all states to 0
        for state in self.all_states:
            self.values[state] = 0.0

        # Run policy evaluation
        for iteration in range(max_iterations):
            print(f"Iteration {iteration+1}...")
            delta = 0.0 # Tracking maximum change in value across all states

            # Use the state-value function to evaluate the policy, improving the values of the states based on the current policy
            for state_key in self.all_states:
                old_value = self.values[state_key]

                # Check for terminal state
                grid = self.game_state_to_grid(state_key)
                game = SingleTic(grid)
                result = game.game_result()

                if result is not None:
                    self.values[state_key] = self.get_reward(state_key, player="X")

                else:
                    policy_action = self.policy[state_key]
                    
                    next_state = self.get_next_state(state_key, policy_action)
                    immediate_reward = self.get_reward(state_key, player="X")
                    future_value = self.values[next_state]

                    # Update the value for the current state
                    self.values[state_key] = immediate_reward + gamma * future_value

                delta = max(delta, abs(self.values[state_key] - old_value))
                    
            print(f"Iteration {iteration+1}, max change: {delta:.6f}")

            if delta < theta:
                print(f"Policy evaluation converged after {iteration+1} iterations")
                return iteration + 1
            
        print(f"Policy evaluation reached maximum number of iterations: {max_iterations}")
        return max_iterations
    
    def policy_improvement(self, gamma=0.9):
        print("=== IMPROVING POLICY ===")
        policy_changed = False


        for state_key in self.all_states:
            grid = self.game_state_to_grid(state_key)
            game = SingleTic(grid)
            result = game.game_result()

            # Skip terminal states
            if result is not None:
                continue
            
            available_actions = self.get_valid_actions(state_key)
            current_player = self.get_current_player(state_key)

            q_values = []
            for action in available_actions:
                next_state = self.get_next_state(state_key, action)
                immediate_reward = self.get_reward(state_key, player="X")
                future_value = self.values[next_state]
                q_value = immediate_reward + gamma * future_value
                q_values.append(q_value)

            # Choose the action with the highest Q-value, depending on the current player
            if current_player == 'X':
                best_action = available_actions[np.argmax(q_values)]
            else:
                best_action = available_actions[np.argmin(q_values)]

            if state_key not in self.policy or self.policy[state_key] != best_action:
                self.policy[state_key] = best_action
                policy_changed = True

        if policy_changed:
            print("Policy changed, continuing...")
            return True
        else:
            print("Policy is stable")
            return False
        
    def run_policy_iteration(self, gamma=0.9, theta=1e-6, max_iterations=20):
        print("Running policy iteration...")

        # Step 1: Initialize policy randomly
        self.initialize_policy()

        for iteration in range(max_iterations):
            print(f"Iteration {iteration+1}...")

            # Step 2: Evaluate the policy
            evaluation_iterations = self.policy_evaluation(gamma, theta)

            # Step 3: Improve the policy
            policy_changed = self.policy_improvement(gamma)

            # Step 4: Check for convergence
            if not policy_changed:
                print(f"\nPolicy iteration converged after {iteration + 1} iterations!")
                print(f"Total policy evaluations: {iteration + 1}")
                return self.policy

        print(f"Policy iteration reached maximum number of iterations: {max_iterations}")
        return self.policy




def test_custom():
    print("--- TESTING CUSTOM STATE ---")

    pi = PolicyIteration()
    policy = pi.run_policy_iteration()
    
    # Create any test state
    test_grid = [['X', 'O', None], 
                ['O', None, None], 
                [None, None, 'X']]
    test_state = tuple(tuple(row) for row in test_grid)

    current_player = pi.get_current_player(test_state)

    print(f"Optimal move for {current_player}: {policy[test_state]}")


    
def main():
    print("=== POLICY ITERATION ===")
    pi = PolicyIteration()
    policy = pi.run_policy_iteration()

    SingleTic.simulate_game(policy)


if __name__ == "__main__":
    main()