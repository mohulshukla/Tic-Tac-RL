import numpy as np
from backend.helpers import position_to_coordinates
import random

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
    

    def game_state_to_grid(self, state_key):
        return [list(row) for row in state_key]
    
    
    def get_valid_actions(self, state_key):
        grid = self.game_state_to_grid(state_key)
        valid_actions = []
        for i in range(9):
            row, col = position_to_coordinates(i)
            if grid[row][col] is None:
                valid_actions.append(i)
        return valid_actions
    
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

    @classmethod
    def simulate_game(cls, policy):
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
        game = cls()
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
                return cls.simulate_game(policy)  # Recursive call for new game
            elif play_again in ['n', 'no']:
                print("Thanks for playing!")
                return result
            else:
                print("Please enter y or n")

    @classmethod
    def simulate_ai_game(cls, policy_X, policy_O):
        """
        Simulate a game between two AI policies: policy_X (for 'X') and policy_O (for 'O').
        Logs each move and the final result, indicating which policy is making each move.
        """
        print("AI vs AI Tic-Tac-Toe!")
        print("="*40)
        print("Policy X vs Policy O")
        print("Positions are numbered 0-8:")
        print("0 | 1 | 2")
        print("---------") 
        print("3 | 4 | 5")
        print("---------")
        print("6 | 7 | 8")
        print()

        def print_board(grid):
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

        def get_ai_move(game, policy, player_label):
            state_key = game.get_state_key()
            if state_key in policy:
                ai_move = policy[state_key]
                print(f"{player_label} chooses position {ai_move}")
                return ai_move
            else:
                print(f"{player_label} couldn't find optimal move, choosing randomly...")
                valid_moves = []
                for i in range(9):
                    row, col = position_to_coordinates(i)
                    if game.grid[row][col] is None:
                        valid_moves.append(i)
                if valid_moves:
                    return random.choice(valid_moves)
                return None

        # Initialize game
        game = cls()
        print_board(game.grid)

        # Game loop
        while game.game_result() is None:
            current_player = game.get_current_player(game.get_state_key())
            if current_player == 'X':
                move = get_ai_move(game, policy_X, "Policy X (X)")
            else:
                move = get_ai_move(game, policy_O, "Policy O (O)")
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
        if result == 'X':
            print("Policy X (X) wins!")
        elif result == 'O':
            print("Policy O (O) wins!")
        elif result == 'D':
            print("It's a draw between Policy X and Policy O!")
        else:
            print("Game ended unexpectedly")
        print("="*40)
        return result

