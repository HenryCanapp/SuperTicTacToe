import board
import superBoard

def get_valid_input(kind = "square"):
    """Gets a valid input"""
    while True:
        try:
            value = int(input(f"Enter which {kind} you would like to go: "))
            if value < 0 or value > 8:
                print("Please enter a number 0-8")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")


def place_value(_board : board.Board, pos, value):
    """Checks if the space on the board is open"""
    return _board.try_place(value, pos)

def pick_board(_super : superBoard.SuperBoard, pos):
    """Checks if that board is availible"""
    return _super.try_pick_board(pos)

def print_start():
    print("Welcome to Tic Tac Toe")
    print("| 0 | 1 | 2 |\n| 3 | 4 | 5 |\n| 6 | 7 | 8 |")

def flip_player(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

def reg_game_loop():
    game = board.Board()
    print_start()
    player = 'X'
    while True:
        print(f"{player}, your turn!")
        position = get_valid_input()
        while not place_value(game, position, player):
            print("Please enter an unoccupied space 0-8")
            position = get_valid_input()
        print(game)
        if game.check_over():
            if game.tie:
                print("Tie!")
            else:
                print(f"{player} wins!")
            return
        player = flip_player(player)

def super_input_prompt(game : superBoard.SuperBoard()):
    super_position = get_valid_input("board")
    while not pick_board(game, super_position):
        print("Please enter an active board 0-8")
        super_position = get_valid_input("board")
    return super_position

def super_game_loop_terminal():
    game = superBoard.SuperBoard()
    print_start()
    player = 'X'
    super_position = 0
    while True:
        print(f"{player}, your turn!")

        #if no board is selected, selct one
        if game.current_board is None:
            super_position = super_input_prompt(game)
        print(game)

        #gets a valid input and places it on the current board
        print(f"{player}", end = " ")
        position = get_valid_input()
        while not place_value(game.current_board, position, player):
            print("Please enter an unoccupied space 0-8")
            position = get_valid_input()
        print(game)

        #if the current board has been completed, change the data
        if game.check_current_board():
            game.place_value(game.current_board.winner, super_position)

        if game.check_over():
            if game.tie:
                print("Tie!")
            else:
                print(f"{player} wins!")
            game.move_board(-1)
            print(game)
            return

        if game.move_board(position):
            super_position = position
        else:
            super_position = None
        print(game)
        player = flip_player(player)


#def
#def super_game_screen_update()