import pygame as pg
from colors import Colors

class Tile:


    def __init__(self, pos = 0, size = 48, separation = 4):
        self.data = '_'
        self.surface = pg.Surface([size, size])
        self.box = pg.rect.Rect((pos % 3) * (size + separation), (pos // 3) * (size + separation), size, size)
        self.separation = separation
        self.confirmed = False

        self.default_background_color = Colors.WHITE
        self.background_color = Colors.WHITE
        self.x_color = Colors.RED
        self.o_color = Colors.BLUE

    def draw_data(self):
        """Draws the X or O or nothing onto the tile's surface"""
        if self.data == 'X':
            pg.draw.line(self.surface, self.x_color, self.surface.get_rect().topleft, self.surface.get_rect().bottomright, self.separation)
            pg.draw.line(self.surface, self.x_color, self.surface.get_rect().topright, self.surface.get_rect().bottomleft, self.separation)
        if self.data == 'O':
            pg.draw.circle(self.surface, self.o_color, self.surface.get_rect().center, self.surface.get_rect().height / 2, self.separation)

    def update_surface(self):
        """Updates the surface:
        -if there is no data (ie it is not selected) set the background to default
        -if it is selected then background is changed to yellow, shows the value, and made transparent
        -if it is confirmed then background is white and shows value"""
        if self.data == '_':
            self.background_color = self.default_background_color
        elif not self.confirmed:
            self.background_color = Colors.YELGRN
        else:
            self.background_color = self.default_background_color
        self.surface.fill(self.background_color)
        self.draw_data()

    def draw_tile(self, base_surface : pg.surface.Surface):
        """Blits the surface onto the base_surface"""
        base_surface.blit(self.surface, self.box.topleft)

    def clicked_on(self, pos):
        """returns whether pos is in the collision box"""
        return self.box.collidepoint(pos)

    def toggle_selected(self, value = '_'):
        """If value is passed in, sets the value to that without confirming
        (essentially selecting), if no value passed, unselected"""
        self.data = value

    def confirm_tile(self):
        """Sets the tile state to be confirmed"""
        self.confirmed = True


class Board:

    #the rect of each board, will always be the same
    def __init__(self, pos = 0, size = 152, separation = 9, line_width = 4, has_tiles = True):
        """A tictactoe board that keeps track of
        what has been placed where. default values are '_'
            use try_place, check_over, and the tie/win properties"""
        self.data = ['_'] * 9
        self.winner = None
        self.surface = pg.Surface([size, size])
        self.box = pg.rect.Rect((pos % 3) * (size + separation), (pos // 3) * (size + separation), size, size)
        self.separation = separation
        self.tile_size = (size - 2 * line_width) // 3
        self.selected = False
        self.next = False
        self.x_color = Colors.RED
        self.o_color = Colors.BLUE

        #list of tiles for drawing purposes
        if has_tiles:
            self.tiles = []
            for i in range(9):
                self.tiles.append(Tile(pos = i, size = self.tile_size, separation=line_width))


    def place_value(self, value, pos):
        """Places the given value at pos,
        pos is 0-8, 0 being top left
        8 being bottom right"""
        self.data[pos] = value
        if hasattr(self, "tiles"):
            self.tiles[pos].confirm_tile()


    def is_unoccupied(self, pos):
        """Checks if pos is available"""
        return True if self.data[pos] == '_' else False

    def try_place(self, value, pos):
        """attempts to place value at pos
        return true if successful, false if not"""
        if pos < 0 or pos > 8:
            return False
        if self.is_unoccupied(pos):
            self.place_value(value, pos)
            return True
        else:
            return False

    def check_over(self):
        """Checks if the game is over and sets the appropriate winner"""

        #Checking cols
        for col in [0, 1, 2]:
            if self.data[col] != '_':
                if self.data[col] == self.data[col + 3] == self.data[col + 6]:
                    self.winner = self.data[col]
                    return True
        #Checking rows
        for row in [0, 3, 6]:
            if self.data[row] != '_':
                if self.data[row] == self.data[row + 1] == self.data[row + 2]:
                    self.winner = self.data[row]
                    return True

        #Checking diagnol
        if self.data[0] != '_':
            if self.data[0] == self.data[4] == self.data[8]:
                self.winner = self.data[0]
                return True

        # Checking anti-diagnol
        if self.data[2] != '_':
            if self.data[2] == self.data[4] == self.data[6]:
                self.winner = self.data[2]
                return True

        # check for tie
        if '_' not in self.data:
            self.winner = 'T'
            return True

        return False

    @property
    def tie(self):
        """Returns True if gamer is a tie"""
        return True if self.winner == 'T' else False

    @property
    def x_won(self):
        """Returns True if X won"""
        return True if self.winner == 'X' else False

    @property
    def o_won(self):
        """returns True if O won"""
        return True if self.winner == 'O' else False

    def str_small(self):
        """returns 3 strings for super formatting"""
        b = self.data

        GREY = '\033[38;5;242m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        RESET = '\033[0m'
        if self.x_won:
            line_one = RED + "|\\   /|" + RESET
            line_two = RED + "|  X  |" + RESET
            line_three = RED + "|/   \\|" + RESET
        elif self.o_won:
            line_one = BLUE + "|/ ̅ \\|" + RESET
            line_two = BLUE + "||   ||" + RESET
            line_three = BLUE + "|\\ _ /|"+RESET
        elif self.tie:
            line_one = GREY + f"|{b[0]}|{b[1]}|{b[2]}|" + RESET
            line_two = GREY + f"|{b[3]}|{b[4]}|{b[5]}|" + RESET
            line_three = GREY + f"|{b[6]}|{b[7]}|{b[8]}|" + RESET
        else:
            line_one = f"|{b[0]}|{b[1]}|{b[2]}|"
            line_two = f"|{b[3]}|{b[4]}|{b[5]}|"
            line_three = f"|{b[6]}|{b[7]}|{b[8]}|"
        return line_one, line_two, line_three

    def __str__(self):
        """returns a pretty board
        | _ | _ | _ |
        | X | O | O |
        | _ | X | O |
        """
        b = self.data
        return f"| {b[0]} | {b[1]} | {b[2]} |\n| {b[3]} | {b[4]} | {b[5]} |\n| {b[6]} | {b[7]} | {b[8]} |"

    def clicked_on(self, pos):
        """returns whether inside the collision box"""
        return self.box.collidepoint(pos)

    def get_tile_clicked(self, pos):
        """Returns the tile that was clicked on"""
        for i in self.tiles:
            if i.clicked_on(pos):
                return i
        return None

    def get_index_clicked(self, pos):
        """Gets the index of the tile clicked"""
        list_pos = (pos[0]-self.box.left,pos[1]-self.box.top)
        for i in range(9):
            if self.tiles[i].clicked_on(list_pos):
                return i
        return -1

    def draw_data(self):
        """Draws the X or O or nothing onto the boards's surface, or draws all the tiles"""
        if self.winner == 'X':
            pg.draw.line(self.surface, self.x_color, self.surface.get_rect().topleft, self.surface.get_rect().bottomright, self.separation)
            pg.draw.line(self.surface, self.x_color, self.surface.get_rect().topright, self.surface.get_rect().bottomleft, self.separation)
        elif self.winner == 'O':
            pg.draw.circle(self.surface, self.o_color, self.surface.get_rect().center, self.surface.get_rect().height / 2, self.separation)

    def update_surface(self):
        """Updates the surface:
        -If the board has been won, set the background to white and draw the winner
        -if the board has been tied, set to be transparent
        -draw all the tiles onto the surface
        -changes the background color of the tiles based on if it is selected or not"""
        self.surface.fill(Colors.BLACK)
        self.surface.set_alpha(255)
        if self.tie:
            self.surface.set_alpha(175)
        if self.x_won or self.o_won:
            self.surface.fill(Colors.WHITE)
            self.draw_data()
        else:
            if self.selected:
                tiles_color = Colors.GREEN
            elif self.next:
                tiles_color = Colors.YELLOW
            else:
                tiles_color = Colors.WHITE
            for i in self.tiles:
                i.default_background_color = tiles_color
                i.update_surface()
                i.draw_tile(self.surface)


    def draw_board(self, base_surface : pg.surface.Surface):
        """Blits the surface onto the base_surface"""
        base_surface.blit(self.surface, self.box.topleft)
