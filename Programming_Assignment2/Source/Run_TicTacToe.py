# This file trains the QLearner, and can also run Tic Tac Toe against the user with the QLearner
# Whether to train the QLearner, or running a Tic Tac Toe game against a user, is specified with command line arguments
# When training the QLearner, it displays the score of the QLearner against 10 runs
# Written by Prathik Sannecy
# 3/10/2020

import Programming_Assignment2.Source.QLearning as QLearning
import Programming_Assignment2.Source.QTable as QTable
import Programming_Assignment2.Source.TicTacToe as TicTacToe
import random

NUM_EPOCHS = 500 # How many epochs to use to train the QLearner
EPOCH = 10 # Decrease the greedy percentage after this many epochs
NUM_EPOCHS_DECREASE_GREEDY = 5 # Decrease the Greediness factor after this many epochs
DECREASE_GREEDY = .01 # Decrease the greedy percentage by this much
INIT_GREEDY = 0.1 # Initial value for how often a greedy selection should be made
RANDOM = 1 # Random player should always make random decision 100% of the time


def run_tic_tac_toe_game(QLearner_player, random_player, random_probability):
    """Runs a game of Tic Tac Toe between a QLearner and a random player

    inputs:
        QLearner QLearner_player: Qlearner player
        QLearner random_player: random player

    returns:
        1 if the QLeaner wins, 0.5 if a tie, 0 if QLearner loses
    """
    global INIT_GREEDY
    global RANDOM
    tic_tac_toe_game = TicTacToe.TicTacToeGame()
    # Keep running until the game ends
    while True:
         # Random player makes a move. Update the QLearner's QTable, and check if the game has ended
        old_state, old_Qvalue, action = random_player.make_move(tic_tac_toe_game, 'X', RANDOM)
        QLearner_player.update_QTable_after_move(old_state, old_Qvalue, action, tic_tac_toe_game, 'O', 'X')
        if tic_tac_toe_game.check_win('X'):
            return QLearning.LOSE_REWARD
        if tic_tac_toe_game.check_tie('O', 'X'):
            return QLearning.TIE_REWARD

       # QLearner makes a move. Update its QTable, and check if the game has ended
        old_state, old_Qvalue, action = QLearner_player.make_move(tic_tac_toe_game, 'O', random_probability)
        QLearner_player.update_QTable_after_move(old_state, old_Qvalue, action, tic_tac_toe_game, 'O', 'X')
        if tic_tac_toe_game.check_win('O'):
            return QLearning.WIN_REWARD
        if tic_tac_toe_game.check_tie('O', 'X'):
            return QLearning.TIE_REWARD

def train_QLearner():
    """Trains the Tic Tac Toe QLearner and writes it to a file for future use

    inputs:
        None

    returns:
        None
    """
    global NUM_EPOCHS
    global EPOCH
    global INIT_GREEDY
    global DECREASE_GREEDY
    global NUM_EPOCHS_DECREASE_GREEDY
    random.seed()
    random_probability = INIT_GREEDY
    # Create the two players
    player1 = QLearning.QLearning()
    player2 = QLearning.QLearning()
    # Keep track of how many games the 'smart' QLearning algorithm won against the random algorithm
    for epoch_number in range(NUM_EPOCHS):
        win_count = 0
        for i in range(EPOCH):
            win_count += run_tic_tac_toe_game(player1, player2, random_probability)
        print("epoch " + str(epoch_number) + ": " + str(win_count/EPOCH))
        if ((epoch_number+1) % NUM_EPOCHS_DECREASE_GREEDY) == 0:
            random_probability = max(0, random_probability - DECREASE_GREEDY)


def main():
    train_QLearner()


if __name__ == '__main__':
    main()
