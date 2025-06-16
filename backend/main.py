import numpy as np
# A 3x3 grid is placed within a larger 3x3 grid. In total, 81 squares are present.

default_grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

class SingleTic:
    def __init__(self, grid=default_grid):
        self.grid = grid

    def flatten_grid(self):
        return [cell for row in self.grid for cell in row]
    
    def non_empty_cells(self):
        return sum(cell is not None for cell in self.flatten_grid())


    def game_result(self):
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
        if not self.check_winner() and self.non_empty_cells() == 9:
            return 'D'
        return -1



class MultiTic:
    def __init__(self):
        self.big_grid = [
            [SingleTic() for _ in range(3)],
            [SingleTic() for _ in range(3)],
            [SingleTic() for _ in range(3)]
        ]

    def _flatten_big_grid(self):
        return [cell for row in self.big_grid for cell in row]
    
    def _grid_index_to_coordinates(self, grid_index):
        if not 0 <= grid_index <= 8:
            raise ValueError("Grid index must be between 0 and 8")
            
        # Convert 1D index to 2D coordinates
        row = grid_index // 3
        col = grid_index % 3
        return row, col
    
    def replace_single_grid(self, grid_index):
        if not 0 <= grid_index <= 8:
            raise ValueError("Grid index must be between 0 and 8")
            
        # Convert 1D index to 2D coordinates
        row, col  = self._grid_index_to_coordinates(grid_index)
        
        grid_to_replace = self.big_grid[row][col]
        
        if isinstance(grid_to_replace, SingleTic):
            result = grid_to_replace.game_result()
            if result:  # Only replace if there's a result (winner or draw)
                self.big_grid[row][col] = result
                return result
        return None
    
    def big_grid_result(self):
        # Create a copy of the big grid with removed SingleTic instances to check for winner
        check_grid = [
            [None if isinstance(cell, SingleTic) else cell for cell in row]
            for row in self.big_grid
        ]

        check_grid = SingleTic(check_grid)
        return check_grid.game_result()
        
    


class Game:
    def __init__(self):
        pass

        
    def make_move(self, x):
        pass

    def exists_valid_move(self, x):
        return True


example = MultiTic()