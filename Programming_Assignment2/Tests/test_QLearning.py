import unittest
from Programming_Assignment2.Source.QLearning import *


class test_QLearning(unittest.TestCase):

    def test_init_QTable(self):
        QTable_init = init_QTable_TicTacToe()
        grid = [
            ['X', 'O', None],
            ['O', 'O', 'X'],
            ['X', 'X', None]
        ]
        location = [0, 2]

        # Make sure the grid is intialized in the QTable, and only one instance is there
        mapped_grid = [match[1] for match in QTable_init if match[0] == [grid, location]]
        assert(mapped_grid == [0])

        grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        location = [0, 0]
        # Make sure the grid is intialized in the QTable, and only one instance is there
        mapped_grid = [match[1] for match in QTable_init if match[0] == [grid, location]]
        assert(mapped_grid == [0])

        assert(len(QTable_init) == 177147) # 27*27*27 different grids x 9 different grid locations


if __name__ == '__main__':
    unittest.main()
