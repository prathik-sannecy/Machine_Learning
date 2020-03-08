import Programming_Assignment2.Source.TicTacToe as TicTacToe
import itertools

def init_QTable_TicTacToe():
    """Initializes the QTable for TicTacToe with all game states and actions = 0

    inputs:
        None

    returns:
        List[List[List[List[char]],List[int, int]], int] QTable: Each [game state, move] maps to 0
    """
    QTable = []
    row = [None, 'X', 'O']
    grid_offset = [0, 1, 2]
    row_combinations = list(map(list, itertools.product(row, repeat=3))) # All possible products of a row (eg [0, None, None])
    grid_locations = list(map(list, itertools.product(grid_offset, repeat=2))) # All possible grid locations (eg [0, 2])
    # Generate every possible grid, and initialize the QTable for that grid=0
    for row1 in row_combinations:
        for row2 in row_combinations:
            for row3 in row_combinations:
                for location in grid_locations:
                    QTable.append([[row1, row2, row3], location, 0])
    return QTable




