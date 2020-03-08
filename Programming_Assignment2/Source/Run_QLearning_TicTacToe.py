import Programming_Assignment2.Source.TicTacToe as TicTacToe
import Programming_Assignment2.Source.QTable as QLearning
import random

init_greedy = 0.1 # Initial value for how often a greedy selection should be made
epoch = 10 # Decrease the greedy percentage after this many epochs
decrease_greedy_per_epoch = .001 # Decrease the greedy percentage by this much

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

