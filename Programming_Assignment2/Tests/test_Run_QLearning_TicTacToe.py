import unittest
from Programming_Assignment2.Source.QTable import *
from Programming_Assignment2.Source.TicTacToe import *
from Programming_Assignment2.Source.Run_QLearning_TicTacToe import *
import copy

class test_Run_QLearning_TicTacToe(unittest.TestCase):
    def test_random_move(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'O', None]
        ]
        orig_game_state = copy.deepcopy(tic_tack_toe.game_state)
        random_move(tic_tack_toe, 'X')
        assert(tic_tack_toe.game_state != orig_game_state)



if __name__ == '__main__':
    unittest.main()