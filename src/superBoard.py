import pygame as pg
import board
from colors import Colors


def new_board():
    return SuperBoard()


class SuperBoard(board.Board):
    def __init__(self):
        super().__init__(size=474, has_tiles=False)
        self.current_board : board.Board() = None
        self.boards = []
        self.next_board = -1
        for i in range(9):
            self.boards.append(board.Board(pos = i))
        #inherits winner variable
        #inherits data list to keep track of each boards winner

    def change_board(self, pos):
        """Changes the current board to the board at pos"""
        self.current_board = self.boards[pos]

    def board_active(self, pos):
        """Checks if that board is still in play"""
        if self.boards[pos].winner is None:
            return True
        return False

    def try_pick_board(self, pos):
        """attempts to change to the board at pos
        returns true of successful, false if not"""
        if pos < 0 or pos > 8:
            return False
        if self.board_active(pos):
            self.change_board(pos)
            return True
        else:
            return False

    def move_board(self, pos):
        """changes the current board based on the move made
        if board is inactive returns false"""
        if self.try_pick_board(pos):
            return True
        else:
            self.current_board = None
            return False

    def check_current_board(self):
        """Checks if the current board has been completed
        if it has return True, if not return False"""
        return self.current_board.check_over()

    def __str__(self):
        """Prints the ENTIRE board in a pretty way
        indicated the current board in yellow"""
        line_one = "|"
        line_two = "|"
        line_three = "|"
        final = "-----------------------\n"
        for i in range(0, 7, 3):
            for j in range(3):
                b = self.boards[i+j]
                if b is self.current_board:
                    YELLOW = '\033[33m'
                    RESET = '\033[0m'
                    one, two, three = b.str_small()
                    line_one += YELLOW + one + RESET
                    line_two += YELLOW + two + RESET
                    line_three += YELLOW + three + RESET
                else:
                    one, two, three = b.str_small()
                    line_one += one
                    line_two += two
                    line_three += three
            final += line_one + "|\n" + line_two + "|\n" + line_three + "|\n"
            final += "-----------------------\n"
            line_one = "|"
            line_two = "|"
            line_three = "|"
        return final

    def get_board_clicked(self, pos):
        """Returns the tile that was clicked on"""
        for i in self.boards:
            if i.clicked_on(pos):
                return i
        return None

    def get_index_clicked(self, pos):
        """Gets the index of the tile clicked"""
        for i in range(9):
            if self.boards[i].clicked_on(pos):
                return i
        return -1

    def current_board_clicked(self, pos):
        if self.current_board is not None:
            return self.current_board.clicked_on(pos)
        return False


    def update_surface(self):
        """Puts all of the boards and their data on the super board"""
        self.surface.fill(Colors.SUPER_LINE_COLOR)
        for i in self.boards:
            if self.next_board > -1 and i is self.boards[self.next_board]:
                i.next = True
                i.selected = False
            elif i is self.current_board:
                i.selected = True
                i.next = False
            else:
                i.selected = False
                i.next = False
            i.update_surface()
            i.draw_board(self.surface)

    def draw_game(self, screen):
        screen.blit(self.surface, [0,0])