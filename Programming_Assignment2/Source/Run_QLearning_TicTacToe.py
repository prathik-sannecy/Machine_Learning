import Programming_Assignment2.Source.TicTacToe as TicTacToe
import Programming_Assignment2.Source.QTable as QTable
import random
import copy

init_greedy = 0.1 # Initial value for how often a greedy selection should be made
epoch = 10 # Decrease the greedy percentage after this many epochs
decrease_greedy_per_epoch = .001 # Decrease the greedy percentage by this much
discount_factor = .8
learning_rate = .05
WIN_REWARD = 1
TIE_REWARD = .5
LOSE_REWARD = 0

def random_move(tic_tac_toe_game:TicTacToe.TicTacToeGame, player):
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
    return current_QTable_value + learning_rate*(reward + discount_factor*next_state_max_QTable_value - current_QTable_value)

def make_move(tic_tac_toe_game:TicTacToe.TicTacToeGame, QTable:QTable.QTable_TicTacToe, player, opponent, random_ratio):
    """Decides what move the player should make. May be random, or may use the QLearning forumula

    inputs:
        TicTacToeGame tic_tac_toe_game: the current state of the tic tac toe game
        QTable QTable: the current QTable being used for tracking rewards for actions
        (char) player: 'X' or 'O'
        (char) opponent: 'X' or 'O'
        float (<1) random_ratio: how often a random move should be take

    returns:
        None
    """
    global WIN_REWARD
    global LOSE_REWARD
    global TIE_REWARD
    old_state = copy.deepcopy(tic_tac_toe_game.get_game_state())
    [action, value] = QTable.max_action_value(tic_tac_toe_game)
    if random.random() < random_ratio:
        random_move(tic_tac_toe_game, player)
    else:
        tic_tac_toe_game.make_move(action, player)
    new_state = copy.deepcopy(tic_tac_toe_game.get_game_state())
    if tic_tac_toe_game.check_tie(player, opponent):
        next_state_max_QTable_value = TIE_REWARD
    elif tic_tac_toe_game.check_win(player):
        next_state_max_QTable_value = WIN_REWARD
    elif tic_tac_toe_game.check_win(opponent):
        next_state_max_QTable_value = LOSE_REWARD
    else:
        [next_state_max_QTable_action, next_state_max_QTable_value] = QTable.max_action_value(tic_tac_toe_game)
    new_QTable_value = calc_new_QTable_value(value, 0, next_state_max_QTable_value)
    QTable.update_state_action_value(old_state, action, new_QTable_value)

