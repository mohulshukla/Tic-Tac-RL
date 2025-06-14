class Game:
    def __init__(self):
        self.board = [None] * 9
        self.current_player = 'X'

    def make_move(self, index):
        if self.board[index] is None:
            self.board[index] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            raise ValueError("Invalid move")