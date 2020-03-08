import unittest
from Programming_Assignment2.Source.TicTacToe import *


class test_TicTacToe(unittest.TestCase):

    def test_display_grid(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'X', None]
        ]
        tic_tack_toe.display_grid()

    def test_test_valid_move(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'X', None]
        ]
        assert(tic_tack_toe.test_valid_move((0, 2)) == True)
        assert(tic_tack_toe.test_valid_move((1, 1)) == False)

    def test_check_full(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'X', None]
        ]
        assert(tic_tack_toe.check_grid_full() == False)
        tic_tack_toe.game_state = [
            ['X', 'O', 'X'],
            ['O', 'O', "X"],
            ['O', 'X', 'O']
        ]
        assert(tic_tack_toe.check_grid_full() == True)

    def test_make_move(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'X', None]
        ]
        assert(tic_tack_toe.make_move([1,0], 'X') == False)
        grid_new = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            ['X', 'X', None]
        ]
        tic_tack_toe.make_move([2, 0], 'X')
        assert(tic_tack_toe.get_game_state() == grid_new)

    def test_check_win(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'O', None]
        ]
        # Check no win
        assert(tic_tack_toe.check_win('X') == False)
        assert(tic_tack_toe.check_win('O') == True)
        tic_tack_toe.game_state = [
            ['O', 'O', 'X'],
            ['O', 'X', "X"],
            ['X', 'O', 'O']
        ]
        # Check diag win
        assert(tic_tack_toe.check_win('X') == True)
        assert(tic_tack_toe.check_win('O') == False)
        tic_tack_toe.game_state = [
            ['O', 'O', 'X'],
            ['O', None, "X"],
            ['O', 'X', 'O']
        ]
        # check column win
        assert(tic_tack_toe.check_win('X') == False)
        assert(tic_tack_toe.check_win('O') == True)



if __name__ == '__main__':
    unittest.main()
