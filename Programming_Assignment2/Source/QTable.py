import Programming_Assignment2.Source.TicTacToe as TicTacToe
import itertools

class QTable_TicTacToe():
    def __init__(self):
        """Initializes the QTable for TicTacToe with all game states and actions = 0

        inputs:
            None

        returns:
            None
        """
        self.QTable = []
        row = [None, 'X', 'O']
        grid_offset = [0, 1, 2]
        row_combinations = list(map(list, itertools.product(row, repeat=3))) # All possible products of a row (eg [0, None, None])
        grid_locations = list(map(list, itertools.product(grid_offset, repeat=2))) # All possible grid locations (eg [0, 2])
        # Generate every possible grid, and initialize the QTable for that grid=0
        for row1 in row_combinations:
            for row2 in row_combinations:
                for row3 in row_combinations:
                    for location in grid_locations:
                        self.QTable.append([[row1, row2, row3], location, 0])


    def get_actions_rewards(self, tic_tac_toe_game:TicTacToe.TicTacToeGame):
        """Returns all the state's actions that are valid and their respective rewards

        inputs:
            TicTacToeGame tic_tac_toe_game: the current state of the tic tac toe game

        returns:
            List[List[List[int, int], int]] action_rewards: all the possible actions from a particular state, and their respective rewards
        """
        return [[action, value] for [state, action, value] in self.QTable if state == tic_tac_toe_game.get_game_state() and tic_tac_toe_game.test_valid_move(action)]

    def max_action_reward(self, tic_tac_toe_game:TicTacToe.TicTacToeGame ):
        """Returns the action and the value that has the largest reward based on being in a particular state

        inputs:
            TicTacToeGame tic_tac_toe_game: the current state of the tic tac toe game

        returns:
            List[List[int, int], int] max_action_reward: the action and reward with that's the largest based on the current state
        """
        # Traverse through all the possible actions in a particular state
        # Pick the action that yields the highest reward
        actions_values = self.get_actions_rewards(tic_tac_toe_game)
        [max_action, max_value] = actions_values[0]
        for action_value in actions_values:
            [action, value] = action_value
            if value > max_value:
                max_action, max_value = action, value
        return [max_action, max_value]

    def update_state_action_reward(self, tic_tac_toe_game:TicTacToe.TicTacToeGame , action, reward):
        """Updates the QTable's state and action with a new reward

        inputs:
            TicTacToeGame tic_tac_toe_game: the current state of the tic tac toe game
            List[int, int] action: the next position to make a move
            int reward: the new updated reward for the QTable

        returns:
            None
        """
        for e in self.QTable:
            [state, state_action, value] = e
            if state == tic_tac_toe_game.game_state and state_action == action:
                e[2] = reward
