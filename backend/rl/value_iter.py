# Value Iteration over a Basic Tic-Tac-Toe game

# The Bellman Equation: 
# V(s) = max_a [R(s,a) + gamma * sum_{s'} P(s'|s,a) * V(s')]

# The Bellman Equation for Value Iteration: 
# V(s) = R(s) + gamma * sum_{s'} P(s'|s,pi(s)) * V(s')

import numpy as np
from backend.helpers import position_to_coordinates
import random
# A 3x3 grid is placed within a larger 3x3 grid. In total, 81 squares are present.


class SingleTic:
    def __init__(self, grid=None):
        if grid is None:
            self.grid  = [[None for _ in range(3)] for _ in range(3)]
        else:
            self.grid = grid

    def flatten_grid(self):
        return [cell for row in self.grid for cell in row]
    
    def non_empty_cells(self):
        return sum(cell is not None for cell in self.flatten_grid())
    
    
    def make_move(self, grid_index, current_player):
        assert current_player in ['X', 'O']
        row, col = position_to_coordinates(grid_index)
        if self.grid[row][col] is not None:
            print("Cell already taken, not making move.")
        self.grid[row][col] = current_player

    def game_result(self):
        # Game cannot end if there are less than 3 cells filled
        if self.non_empty_cells() < 3:
            return None
        
        return self._check_winner() or self._check_draw()

    def _check_winner(self):
        grid = np.array(self.grid)
        
        # Get all possible winning lines
        lines = [
            *grid,                    # rows
            *grid.T,                  # columns
            grid.diagonal(),          # main diagonal
            np.fliplr(grid).diagonal() # anti-diagonal
        ]
        
        # Check each line for a winner
        for line in lines:
            if all(x == line[0] and x is not None for x in line):
                return line[0]
                
        return None
    
    def _check_draw(self):
        if not self._check_winner() and self.non_empty_cells() == 9:
            return 'D'
        return None
    
    def get_state_key(self):
        return tuple(tuple(row) for row in self.grid)
    
    # This is a recursive function that generates all possible states of the game
    def get_all_states(self):
        all_states = set()

        def generate_recursive(grid, current_player):
            # Create an initial state
            state = SingleTic(grid)
            all_states.add(state.get_state_key())

            if state.game_result() is not None:
                return

            # Get all possible moves for the current player
            for i in range(9):
                row, col = position_to_coordinates(i)
                if grid[row][col] is None:
                    # Make a copy of the grid, and place the current player in the new grid
                    new_grid = [row[:] for row in grid]
                    new_grid[row][col] = current_player

                    # Recurse with the new grid and the other player
                    next_player = 'O' if current_player == 'X' else 'X'
                    generate_recursive(new_grid, next_player)

        empty_grid = [[None for _ in range(3)] for _ in range(3)]
        generate_recursive(empty_grid, 'X')
        return all_states
    
    def get_current_player(self, state_key):
        grid = [list(row) for row in state_key]
        x_count = sum(row.count('X') for row in grid)
        o_count = sum(row.count('O') for row in grid)

        if x_count == o_count:
            return 'X'
        elif x_count == o_count + 1:
            return 'O'
        else:
            # This shouldn't happen in a valid game
            raise ValueError(f"Invalid game state: X={x_count}, O={o_count}")


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


def simulate_game(policy):
    """
    Interactive game where human plays against the optimal AI policy
    """
    print("Welcome to Tic-Tac-Toe vs Optimal AI!")
    print("="*40)
    
    # Let human choose their symbol
    while True:
        human_choice = input("Do you want to play as X or O? (X/O): ").upper().strip()
        if human_choice in ['X', 'O']:
            break
        print("Please enter X or O")
    
    ai_choice = 'O' if human_choice == 'X' else 'X'
    print(f"\nYou are {human_choice}, AI is {ai_choice}")
    print("Positions are numbered 0-8:")
    print("0 | 1 | 2")
    print("---------") 
    print("3 | 4 | 5")
    print("---------")
    print("6 | 7 | 8")
    print()
    
    def print_board(grid):
        """Print the current board in a nice format"""
        print("\nCurrent board:")
        for i in range(3):
            row_str = ""
            for j in range(3):
                cell = grid[i][j]
                if cell is None:
                    cell = " "
                row_str += f" {cell} "
                if j < 2:
                    row_str += "|"
            print(row_str)
            if i < 2:
                print("-----------")
        print()
    
    def get_human_move(game):
        """Get a valid move from the human player"""
        while True:
            try:
                print(f"Your turn ({human_choice})!")
                move = int(input("Enter position (0-8): "))
                
                if move < 0 or move > 8:
                    print("Position must be between 0-8")
                    continue
                
                row, col = position_to_coordinates(move)
                if game.grid[row][col] is not None:
                    print("That position is already taken!")
                    continue
                
                return move
                
            except ValueError:
                print("Please enter a valid number (0-8)")
    
    def get_ai_move(game, policy):
        """Get the optimal move from the AI"""
        state_key = game.get_state_key()
        
        if state_key in policy:
            ai_move = policy[state_key]
            print(f"AI ({ai_choice}) chooses position {ai_move}")
            return ai_move
        else:
            # This shouldn't happen with a complete policy, but just in case
            print("AI couldn't find optimal move, choosing randomly...")
            valid_moves = []
            for i in range(9):
                row, col = position_to_coordinates(i)
                if game.grid[row][col] is None:
                    valid_moves.append(i)
            if valid_moves:
                import random
                return random.choice(valid_moves)
            return None
    
    # Initialize game and start playing
    game = SingleTic()
    print_board(game.grid)
    
    # Game loop
    while game.game_result() is None:
        current_player = game.get_current_player(game.get_state_key())
        
        if current_player == human_choice:
            # Human's turn
            move = get_human_move(game)
            game.make_move(move, current_player)
        else:
            # AI's turn
            move = get_ai_move(game, policy)
            if move is not None:
                game.make_move(move, current_player)
            else:
                print("No valid moves available!")
                break
        
        print_board(game.grid)
    
    # Announce the result
    result = game.game_result()
    print("="*40)
    print("GAME OVER!")
    
    if result == human_choice:
        print("🎉 Congratulations! You won!")
        print("(This shouldn't happen if the AI is truly optimal...)")
    elif result == ai_choice:
        print("🤖 AI wins! The optimal strategy prevails!")
    elif result == 'D':
        print("🤝 It's a draw! Well played against the optimal strategy!")
    else:
        print("Game ended unexpectedly")
    
    print("="*40)
    
    # Ask if they want to play again
    while True:
        play_again = input("Want to play again? (y/n): ").lower().strip()
        if play_again in ['y', 'yes']:
            print("\n" + "="*50 + "\n")
            return simulate_game(policy)  # Recursive call for new game
        elif play_again in ['n', 'no']:
            print("Thanks for playing!")
            return result
        else:
            print("Please enter y or n")


def main():
    vi = ValueIteration()
    policy = vi.run_value_iteration()
    simulate_game(policy)
    
if __name__ == "__main__":
    main()