import board

def get_valid_input():
    """Gets a valid input"""
    while True:
        try:
            value = int(input("Enter where you would like to go: "))
            if value < 0 or value > 8:
                print("Please enter a number 0-8")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")



def place_value(_board : board.Board, pos, value):
    """Checks if the space on the board is open"""
    return _board.try_place(value, pos)

def print_start():
    print("Welcome to Tic Tac Toe")
    print("| 0 | 1 | 2 |\n| 3 | 4 | 5 |\n| 6 | 7 | 8 |")

def flip_player(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

def game_loop():
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