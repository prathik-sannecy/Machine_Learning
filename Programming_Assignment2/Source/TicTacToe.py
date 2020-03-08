import numpy

class TicTacToeGame():

    def __init__(self):
        self.game_state = [[None]*3 for _ in range(3)]

    def display_grid(self):
        """Prints Tic Tac Toe grid
    
        inputs:
            None
    
        returns:
            None
        """
        for row in self.game_state:
            grid_row = [' ' if e is None else e for e in row]
            print('|'.join(grid_row))
    
    def test_valid_move(self, move):
        """Tests if a tic tack toe move is valid or not
    
        inputs:
            list[int, int] move: the grid location of the next move
    
        returns:
            True if the move is valid, False otherwise
        """
        if self.game_state[move[0]][move[1]] is not None:
            return False
        return True
    
    def check_win(self, player):
        """Checks whether a player has won or not
    
        inputs:
            (char) player: which player to check has wone
    
        returns:
            True if the player has won, False otherwise
        """
        pass
    
    
    def check_full(self):
        """Checks whether the grid is full
    
        inputs:
            None
    
        returns:
            True if the grid is full (no empty spots), False otherwise
        """
        for row in self.game_state:
            for e in row:
                if e is None:
                    return False
        return True
    
    def make_move(self, move, player):
        """A player makes a move on the grid
    
        inputs:
            (char) player: the player making the move
            list[int, int] move: the grid location of the players move
    
        returns:
            False if the move is not valid, or the new updated grid with the player's move
        """
        if not self.test_valid_move( move):
            return False
        self.game_state[move[0]][move[1]] = player

    def get_game_state(self):
        return self.game_state
    
    
