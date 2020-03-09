import Programming_Assignment2.Source.QLearning as QLearning
import Programming_Assignment2.Source.QTable as QTable
import Programming_Assignment2.Source.TicTacToe as TicTacToe

NUM_EPOCHS = 2
EPOCH = 10 # Decrease the greedy percentage after this many epochs
DECREASE_GREEDY_PER_EPOCH = .001 # Decrease the greedy percentage by this much
INIT_GREEDY = 0.1 # Initial value for how often a greedy selection should be made
RANDOM = 1 # Random player should always make random decision 100% of the time


def run_tic_tac_toe_game(QLearner_player, random_player):
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
        # QLearner makes a move. Update its QTable, and check if the game has ended
        old_state, old_Qvalue, action = QLearner_player.make_move(tic_tac_toe_game, 'X', INIT_GREEDY)
        QLearner_player.update_QTable_after_move(old_state, old_Qvalue, action, tic_tac_toe_game, 'X', 'O')
        if tic_tac_toe_game.check_win('X'):
            return QLearning.WIN_REWARD
        if tic_tac_toe_game.check_tie('X', 'O'):
            return QLearning.TIE_REWARD
        # Random player makes a move. Update the QLearner's QTable, and check if the game has ended
        old_state, old_Qvalue, action = random_player.make_move(tic_tac_toe_game, 'O', RANDOM)
        QLearner_player.update_QTable_after_move(old_state, old_Qvalue, action, tic_tac_toe_game, 'X', 'O')
        if tic_tac_toe_game.check_win('O'):
            return QLearning.LOSE_REWARD
        if tic_tac_toe_game.check_tie('X', 'O'):
            return QLearning.TIE_REWARD


def main():
    global NUM_EPOCHS
    global EPOCH
    # Create the two players
    player1 = QLearning.QLearning()
    player2 = QLearning.QLearning()
    # Keep track of how many games the 'smart' QLearning algorithm won against the random algorithm
    for j in range(NUM_EPOCHS):
        win_count = 0
        for i in range(EPOCH):
            win_count += run_tic_tac_toe_game(player1, player2)
        print(str(win_count/EPOCH))



if __name__ == '__main__':
    main()