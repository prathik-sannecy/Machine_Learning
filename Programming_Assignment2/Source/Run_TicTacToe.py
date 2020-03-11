# This file trains the QLearner, and can also run Tic Tac Toe against the user with the QLearner
# Whether to train the QLearner, or running a Tic Tac Toe game against a user, is specified with command line arguments
# When training the QLearner, it displays the score of the QLearner against 10 runs
# Written by Prathik Sannecy
# 3/10/2020

import Programming_Assignment2.Source.QLearning as QLearning
import Programming_Assignment2.Source.QTable as QTable
import Programming_Assignment2.Source.TicTacToe as TicTacToe
import random
import sys
import json

NUM_EPOCHS = 500 # How many epochs to use to train the QLearner
EPOCH = 10 # Decrease the greedy percentage after this many epochs
NUM_EPOCHS_DECREASE_GREEDY = 5 # Decrease the Greediness factor after this many epochs
DECREASE_GREEDY = .01 # Decrease the greedy percentage by this much
INIT_GREEDY = 0.1 # Initial value for how often a greedy selection should be made
RANDOM = 1 # Random player should always make random decision 100% of the time
QTable_file = 'Tic_Tac_Toe_QLearner.txt'

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
    global QTable_file
    random.seed()
    random_probability = INIT_GREEDY
    # Create the two players, one QLearner and one random
    QLearner_player = QLearning.QLearning()
    random_player = QLearning.QLearning()
    # Keep track of how many games the 'smart' QLearning algorithm won against the random algorithm
    for epoch_number in range(NUM_EPOCHS):
        win_count = 0
        for i in range(EPOCH):
            win_count += run_tic_tac_toe_game(QLearner_player, random_player, random_probability)
        print("epoch " + str(epoch_number) + ": " + str(win_count/EPOCH))
        if ((epoch_number+1) % NUM_EPOCHS_DECREASE_GREEDY) == 0:
            random_probability = max(0, random_probability - DECREASE_GREEDY)
    print("New Q Table trained!")


    with open(QTable_file, "w+") as QLearner_file:
        json.dump(QLearner_player.QTable.QTable, QLearner_file)
        # for e in QLearner_player.QTable.QTable:
        #     QLearner_file.write(str(e) + '\n')

def play_QLearner():
    """Allows the user to play against the QLearning algorithm agent

    inputs:
        None

    returns:
        None
    """
    def read_QTable():
        """Read in a trained QTable

        inputs:
            None

        returns:
            The previously stored QTable
        """
        global QTable_file
        input_QTable = []
        with open(QTable_file) as input_QTable_file:
            input_QTable = json.load(input_QTable_file)
            # for e in QTable_file:
            #
            #     input_QTable.append(json.load(e))
        return input_QTable

    player = QLearning.QLearning()
    player.QTable.QTable = read_QTable()
    tic_tac_toe_game = TicTacToe.TicTacToeGame()
    tic_tac_toe_game.display_grid()
    # Keep running until the game ends
    while True:
        # User makes a move. Check if the game has ended
        print("Your move")
        valid_move = False
        while valid_move == False: # Make sure the user has entered a valid move
            try:
                user_input = input("Enter where to place 'X' in the form of: row(0-2), column(0-2)\n").strip()
                action = [int(user_input.split(",")[0]), int(user_input.split(",")[1])]
                valid_move = tic_tac_toe_game.make_move(action, 'X')
                if valid_move == False:
                    print("That spot is taken!")
            except:
                print("Please make a valid move!")
        if tic_tac_toe_game.check_win('X'):
            print("X Wins!")
            return
        if tic_tac_toe_game.check_tie('O', 'X'):
            print("Tie game")
            return
        tic_tac_toe_game.display_grid()

        print("Computer move: ")

        # QLearner makes a move. Check if the game has ended
        player.make_move(tic_tac_toe_game, 'O', 0)
        if tic_tac_toe_game.check_win('O') :
            print("O Wins!")
            return
        if tic_tac_toe_game.check_tie('O', 'X'):
            print("Tie game")
            return
        tic_tac_toe_game.display_grid()


def main():
    def user_help_function():
        print("Play Tic Tac Toe against a QLearning algorithm")
        print("Use case: python3 -m Programming_Assignment2.Source.Run_TicTacToe [train]")
        print("Use the 'train' option to reset the Q Table")
        print("Otherwise, will allow user to play Tic Tac Toe")

    if len(sys.argv) > 1:
        if sys.argv[1] == "train":
            train_QLearner()
        else:
            user_help_function()
    else:
        play_QLearner()


if __name__ == '__main__':
    main()
