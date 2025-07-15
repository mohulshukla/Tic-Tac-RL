import numpy as np
from backend.helpers import position_to_coordinates
from backend.rl.single_tic import SingleTic
# A 3x3 grid is placed within a larger 3x3 grid. In total, 81 squares are present.

class MultiTic:
    def __init__(self):
        self.big_grid = [
            [SingleTic() for _ in range(3)],
            [SingleTic() for _ in range(3)],
            [SingleTic() for _ in range(3)]
        ]

    def _flatten_big_grid(self):
        return [cell for row in self.big_grid for cell in row]
    
    def replace_single_grid(self, grid_index):
        if not 0 <= grid_index <= 8:
            raise ValueError("Grid index must be between 0 and 8")
            
        # Convert 1D index to 2D coordinates
        row, col  = position_to_coordinates(grid_index)
        
        grid_to_replace = self.big_grid[row][col]
        
        if isinstance(grid_to_replace, SingleTic):
            result = grid_to_replace.game_result()
            if result:  # Only replace if there's a result (winner or draw)
                self.big_grid[row][col] = result
                return result
        return None
    
    def big_grid_result(self):
        # Create a copy of the big grid with removed SingleTic instances to check for winner --> review if this is correct
        check_grid = [
            [None if isinstance(cell, SingleTic) else cell for cell in row]
            for row in self.big_grid
        ]

        # print(check_grid)

        check_grid = SingleTic(check_grid)
        return check_grid.game_result()
    
    def make_move(self, grid_index, position, current_player):
        big_grid_row, big_grid_col = position_to_coordinates(grid_index)
        single_grid_act = self.big_grid[big_grid_row][big_grid_col]
        if isinstance(single_grid_act, SingleTic):
            single_grid_act.make_move(position, current_player)
            # Returns next player and the next grid_index to play in
            next_player = 'O' if current_player == 'X' else 'X'
            next_grid_index = position
            return next_player, next_grid_index
        else:
            print("Can't make a move on a finished grid")
            return None
        

def pick_position(current_player):
    pos = int(input(f"Pick a position, player {current_player}: "))
    return pos

def pick_grid_index(current_player):
    pos = int(input(f"Pick a new grid index, player {current_player}: "))
    return pos


def game_loop():
    game = MultiTic()
    
    # First player who is X can move anywhere, any grid_index and positon within that grid index
    current_player = 'X'
    first_grid_index = 4 # middle of the big grid, so first player plays in the middle tic tac toe grid
    first_position = pick_position(current_player)
    print(f"Player {current_player} making move in grid {first_grid_index} at position {first_position}")
    
    next_player, next_grid_index = game.make_move(first_grid_index, first_position, current_player)
    
    while True:
        # The game loop
        # See if the grid that the player played in can be replaced by a result from the singular tic tac toe grid
        game.replace_single_grid(next_grid_index)

        # Second player who is 0 moves in the grid_index corresponding to the previous player's position
        # Next player moves in the grid_index corresponding to the previous player's position
        picked_position = pick_position(next_player)
        print(f"Player {next_player} making move in grid {next_grid_index} at position {picked_position}")
        next_player, next_grid_index = game.make_move(next_grid_index, picked_position, next_player)

        # Check to see if that grid can be evaluted for a winner
        if game.big_grid_result():
            print(f"Game over, {next_player} wins!")
            break

        if game.big_grid_result() == 'D':
            print("Game over, draw!")
            break

        # If the next game index is already filled, then the player has to pick a new grid index
        row, col = position_to_coordinates(next_grid_index)
        if not isinstance(game.big_grid[row][col], SingleTic):
           next_grid_index = pick_grid_index(next_player)
            


        
    
if __name__ == "__main__":
    game_loop()

