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

    def test_random_move2(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', 'O'],
            ['O', 'O', 'X'],
            ['X', 'X', None]
        ]

        orig_game_state = copy.deepcopy(tic_tack_toe.game_state)
        QTable = QTable_TicTacToe()
        make_move(tic_tack_toe,QTable, 'X', 'O', 1)
        assert([match[2] for match in QTable.QTable if match[0] == orig_game_state and match[1] == [2,2]][0] > 0)

    def test_calc_new_QTable_value(self):
        assert (calc_new_QTable_value(4, 0,  8) == 4.12)

    def test_make_move(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, None, None]
        ]
        orig_game_state = copy.deepcopy(tic_tack_toe.game_state)
        QTable = QTable_TicTacToe()
        QTable.update_state_action_value(tic_tack_toe.game_state, [2, 1], .7)
        make_move(tic_tack_toe,QTable, 'O', 'X', 0)
        assert([match[2] for match in QTable.QTable if match[0] == orig_game_state and match[1] == [2,1]][0] > .7)

    def test_make_move2(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', None, "X"],
            [None, None, None]
        ]
        next_game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, None, None]
        ]
        orig_game_state = copy.deepcopy(tic_tack_toe.game_state)
        QTable = QTable_TicTacToe()
        QTable.update_state_action_value(tic_tack_toe.game_state, [1, 1], .2)
        QTable.update_state_action_value(next_game_state, [2, 1], .7)
        make_move(tic_tack_toe,QTable, 'O', 'X', 0)
        assert([match[2] for match in QTable.QTable if match[0] == orig_game_state and match[1] == [1,1]][0] > .2)

if __name__ == '__main__':
    unittest.main()