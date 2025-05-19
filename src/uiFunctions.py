import board
import superBoard
import menu
import pygame as pg

from terminalFunctions import place_value, pick_board, flip_player

class GameUI:
    def __init__(self):
        self.go_anywhere = True
        self.picking_board = True
        self.game_over = False
        self.game = superBoard.SuperBoard()
        self.menu = menu.Menu()
        self.player = 'X'
        #what tile was last clicked
        self.last_position = -1
        self.position = -1
        self.super_position = -1
        self.selected_board = -1
        self.menu_clicked = False

    def reset_game(self):
        self.go_anywhere = True
        self.picking_board = True
        self.game_over = False
        self.game = superBoard.SuperBoard()
        self.player = 'X'
        self.last_position = -1
        self.position = -1
        self.super_position = -1
        self.selected_board = -1
        self.menu_clicked = False

    def find_what_clicked(self, pos):
        """finds what on the board was clicked and sets appropriate values"""
        # checks if the click was on the board
        if not self.game_over and self.game.clicked_on(pos):

            # if in board selection mode, select that board
            if self.picking_board:
                # sets the super position to the board clicked, if invalid sets to -1
                self.selected_board = self.game.get_index_clicked(pos)

            # if not in board selection mode, check if clicked on the current selected board
            elif self.game.current_board_clicked(pos):
                # sets the position to the position clicked, if invalid sets to -1
                self.position = self.game.current_board.get_index_clicked(pos)

            # if not clicked on the current selected board, but go_anywhere, switch to that board
            elif self.go_anywhere:
                # sets the super position to the board clicked, if invalid sets to -1
                self.selected_board = self.game.get_index_clicked(pos)
        else: self.menu_clicked = self.menu.clicked_on(pos)


    def evaluate_state(self):
        """Based on the current state of the game and values, adjusts the board
        -returns true if player took their turn"""
        if self.position > -1:

            if self.position == self.last_position:
                #if the tile clicked was the same as the last tile clicked, lock in that tile

                self.game.current_board.try_place(self.player, self.position)
                self.last_position = -1
                self.game.next_board = -1
                return True

            elif self.game.current_board.is_unoccupied(self.position):
                #if the tile that was just clicked is unnocupied, select that tile, and unselect any previous tile
                self.game.current_board.tiles[self.position].toggle_selected(self.player)
                if self.last_position > -1:
                    self.game.current_board.tiles[self.last_position].toggle_selected()
                self.last_position = self.position


        if self.selected_board > -1:
            if self.game.try_pick_board(self.selected_board):
                if self.last_position > -1 and self.super_position > -1:
                    self.game.boards[self.super_position].tiles[self.last_position].toggle_selected()
                    self.last_position = -1
                self.super_position = self.selected_board
                self.picking_board = False
        self.game.next_board = self.last_position

        if self.menu_clicked:
            self.reset_game()


        return False

    def change_state(self):

        # if the current board has been completed, change the data
        if self.game.check_current_board():
            self.game.place_value(self.game.current_board.winner, self.super_position)

        if self.game.check_over():
            self.menu.winner_text(self.game.winner)
            self.game_over = True
            return

        if self.game.move_board(self.position):
            self.super_position = self.position
            self.go_anywhere = False
            self.picking_board = False
        else:
            self.super_position = -1
            self.go_anywhere = True
            self.picking_board = True
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'


    def update_game_state(self, pos = None):
        if pos is None:
            return False

        #update the position values
        self.find_what_clicked(pos)

        #waits till player takes their turn
        if self.evaluate_state():
            self.change_state()

        self.selected_board = -1
        self.position = -1

    def draw_game(self, screen : pg.surface.Surface):
        self.game.update_surface()
        self.menu.update_menu(self.player)
        self.game.draw_game(screen)
        self.menu.draw_menu(screen)
