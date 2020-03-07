import unittest
from Programming_Assignment2.Source.TicTacToe import *


class test_TicTacToe(unittest.TestCase):
    def test_display_grid(self):
        grid = [
            ['X', 'O', None],
            ['O', 'O', "X"],
            [None, 'X', None]
        ]
        display_grid(grid)


if __name__ == '__main__':
    unittest.main()
