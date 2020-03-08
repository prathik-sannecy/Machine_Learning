import unittest
from Programming_Assignment2.Source.QLearning import *
from Programming_Assignment2.Source.TicTacToe import *

class test_QLearning(unittest.TestCase):

    def test_init_QTable(self):
        QTable = QTable_TicTacToe()
        grid = [
            ['X', 'O', None],
            ['O', 'O', 'X'],
            ['X', 'X', None]
        ]
        location = [0, 2]

        # Make sure the grid is intialized in the QTable, and only one instance is there
        mapped_grid = [match[2] for match in QTable.QTable if match[0] == grid and match[1] == location]
        assert(mapped_grid == [0])

        grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        location = [0, 0]
        # Make sure the grid is intialized in the QTable, and only one instance is there
        mapped_grid = [match[2] for match in QTable.QTable if match[0] == grid and match[1] == location]
        assert(mapped_grid == [0])

        assert(len(QTable.QTable) == 177147) # 27*27*27 different grids x 9 different grid locations

    def test_get_actions_rewards(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'X', None]
        ]
        QTable = QTable_TicTacToe()
        assert(QTable.get_actions_rewards(tic_tack_toe) == [[[0, 2], 0], [[2, 0], 0], [[2, 2], 0]])

    def test_max_action_reward(self):
        tic_tack_toe = TicTacToeGame()
        tic_tack_toe.game_state = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'X', None]
        ]
        QTable = QTable_TicTacToe()
        QTable.update_state_action_reward(tic_tack_toe,[2, 2], 4)
        assert(QTable.max_action_reward(tic_tack_toe) == [[2, 2], 4])



if __name__ == '__main__':
    unittest.main()
