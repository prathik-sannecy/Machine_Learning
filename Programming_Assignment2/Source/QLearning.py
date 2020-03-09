import Programming_Assignment2.Source.TicTacToe as TicTacToe
import Programming_Assignment2.Source.QTable as QTable
import random
import copy

discount_factor = .8
learning_rate = .05
WIN_REWARD = 1
TIE_REWARD = .5
LOSE_REWARD = 0

class QLearning():
    def __init__(self):
        self.QTable = QTable.QTable_TicTacToe()

    def random_move(self, tic_tac_toe_game:TicTacToe.TicTacToeGame, player):
        """A player does a random move in the game

        inputs:
            TicTacToeGame tic_tac_toe_game: the current state of the tic tac toe game
            player: the player's turn ('X' or 'O')

        returns:
            None
        """
        move_valid = False
        while move_valid == False:
            move_valid = tic_tac_toe_game.make_move([random.randrange(3), random.randrange(3)], player)


    def make_move(self, tic_tac_toe_game:TicTacToe.TicTacToeGame, player, random_ratio):
        """Decides what move the player should make. May be random, or may use the QLearning formula

        inputs:
            TicTacToeGame tic_tac_toe_game: the current state of the tic tac toe game
            (char) player: 'X' or 'O'
            float (<1) random_ratio: how often a random move should be take

        returns:
            List[List[char]] old_state: the game's grid before the move was made
            int old_QValue: the QValue for the state and action before the action was made
            List[int, int] action: the move that the player took
        """
        # Store the current state of the game prior to making a move
        old_state = copy.deepcopy(tic_tac_toe_game.get_game_state())
        [action, old_Qvalue] = self.QTable.max_action_value(tic_tac_toe_game)
        if random.random() < random_ratio:
            self.random_move(tic_tac_toe_game, player)
        else:
            tic_tac_toe_game.make_move(action, player)
        # Return the prior state of the game (for updating QValue)
        return old_state, old_Qvalue, action

    def update_QTable_after_move(self, old_state, old_value, action, tic_tac_toe_game:TicTacToe.TicTacToeGame, player, opponent):
        """Updates the QTable for the previous state and action after a move has been made

        inputs:
            TicTacToeGame tic_tac_toe_game: the current state of the tic tac toe game
            (char) player: 'X' or 'O'
            (char) opponent: 'X' or 'O'
            List[List[char]] old_state: the game's grid before the move was made
            int old_QValue: the QValue for the state and action before the action was made
            List[int, int] action: the move that the player took

        returns:
            List[List[char]] old_state: the game's grid before the move was made
            int old_QValue: the QValue for the state and action before the action was made
            List[int, int] action: the move that the player took
        """
        def calc_new_QTable_value(current_QTable_value, reward, next_state_max_QTable_value):
            """Performs the formula:
                new_QTable_value = current_QTable_value + learning_rate*(reword + discount_factor*next_state_max_QTable_value - current_QTable_value)

            inputs:
                all floats

            returns:
                float new_QTable_value: the updated QTable value for a current state and action
            """
            global discount_factor
            global learning_rate
            return current_QTable_value + learning_rate * (
                        reward + discount_factor * next_state_max_QTable_value - current_QTable_value)

        global WIN_REWARD
        global LOSE_REWARD
        global TIE_REWARD
        # Figure out what the Reward is. If it's terminated, choose the termination value.
        # Otherwise, use the next state with next action value
        if tic_tac_toe_game.check_tie(player, opponent):
            next_state_max_QTable_value = TIE_REWARD
        elif tic_tac_toe_game.check_win(player):
            next_state_max_QTable_value = WIN_REWARD
        elif tic_tac_toe_game.check_win(opponent):
            next_state_max_QTable_value = LOSE_REWARD
        else:
            [next_state_max_QTable_action, next_state_max_QTable_value] = self.QTable.max_action_value(tic_tac_toe_game)
        # Update the QTable value for the old state using the information gained from the new state
        new_QTable_value = calc_new_QTable_value(old_value, 0, next_state_max_QTable_value)
        self.QTable.update_state_action_value(old_state, action, new_QTable_value)
