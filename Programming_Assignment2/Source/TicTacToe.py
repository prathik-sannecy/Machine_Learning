def display_grid(game_state):
    for row in game_state:
        grid_row = [' ' if e is None else e for e in row]
        print('|'.join(grid_row))