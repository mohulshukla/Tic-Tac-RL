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

