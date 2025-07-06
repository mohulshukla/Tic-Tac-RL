# Value Iteration over a Basic Tic-Tac-Toe game

# The Bellman Equation: 
# V(s) = max_a [R(s,a) + gamma * sum_{s'} P(s'|s,a) * V(s')]

# The Bellman Equation for Value Iteration: 
# V(s) = R(s) + gamma * sum_{s'} P(s'|s,pi(s)) * V(s')

import numpy as np
from backend.helpers import position_to_coordinates
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
            raise ValueError("Cell already taken")
        self.grid[row][col] = current_player

    def game_result(self):
        # Game cannot end if there are less than 3 cells filled
        if self.non_empty_cells() < 3:
            return 0
        
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
        return 0
    
    def get_state_key(self):
        return tuple(tuple(row) for row in self.grid)
    

# Loop to try stuff out
game = SingleTic()
print(game.get_state_key())







