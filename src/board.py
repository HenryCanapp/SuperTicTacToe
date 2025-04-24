class Board:
    def __init__(self):
        self.data = ['_'] * 9
        self.winner = None

    def place_value(self, value, pos):
        """Places the given value at pos,
        pos is 0-8, 0 being top left
        8 being bottom right"""
        self.data[pos] = value

    ''' I want to make this overload work without having to import multiple dispatch
    def place_value(self, value, col_i, row_i):
        self.data[col_i + row_i * 3] = value
    '''

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

    def __str__(self):
        """returns a pretty board
        | _ | _ | _ |
        | X | O | O |
        | _ | X | O |
        """
        b = self.data
        return f"| {b[0]} | {b[1]} | {b[2]} |\n| {b[3]} | {b[4]} | {b[5]} |\n| {b[6]} | {b[7]} | {b[8]} |"

    def check_over(self):
        """Checks if the game is over and sets the appropriate winner"""

        #check for tie
        if '_' not in self.data:
            self.winner = '_'
            return True

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

        return False

    @property
    def tie(self):
        """Returns True if gamer is a tie"""
        return True if self.winner == '_' else False

    @property
    def x_won(self):
        """Returns True if X won"""
        return True if self.winner == 'X' else False

    @property
    def o_won(self):
        """returns True if O won"""
        return True if self.winner == 'O' else False