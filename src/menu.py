import pygame as pg
import os
from colors import Colors

class Menu:
    def __init__(self):

        pg.font.init()

        #box for the whole menu area
        self.box = pg.rect.Rect(0, 474, 474, 166)
        self.surface = pg.Surface(self.box.size)


        self.font = pg.font.Font(os.path.join(os.getcwd(),'files', 'RobotoSlab-VariableFont_wght.ttf'),18)
        self.font.set_bold(True)
        self.player_font = pg.font.Font(os.path.join(os.getcwd(),'files', 'RobotoSlab-VariableFont_wght.ttf'),36)
        self.player_font.set_bold(True)

        # surface for displaying text
        self.message_surface = pg.Surface((self.box.width // 3, 78))
        self.background_color = Colors.MENU_BG
        self.display_color = Colors.MENU_BUTTON
        self.player_x = self.player_font.render("X", True, Colors.X_COLOR)
        self.player_o = self.player_font.render("O", True, Colors.O_COLOR)
        self.displayed_player = self.player_x
        self.message_text = self.font.render("Your Turn!", True, Colors.WHITE)

        #new game button
        self.reset_box = pg.rect.Rect(158,99,158,33)
        self.reset_global_box = pg.rect.Rect(158, 573, 158, 33)
        self.reset_surface = pg.Surface(self.reset_box.size)
        self.reset_surface.fill(Colors.MENU_BUTTON)
        self.reset_surface.blit(self.font.render("New Game", True, Colors.WHITE), (33,3))
        self.reset = False

    def winner_text(self, winner):
        if winner == "T":
            self.message_text = self.font.render(" Tie Game!", True, Colors.WHITE)
        else:
            self.message_text = self.font.render("   Wins!  ", True, Colors.WHITE)



    def clicked_on(self, pos):
        if self.box.collidepoint(pos) and self.reset_global_box.collidepoint(pos):
            self.reset = True
            return True
        return False

    def update_menu(self, player):
        if self.reset:
            self.displayed_player = self.player_x
            self.message_text = self.font.render("Your Turn!", True, Colors.WHITE)
            self.reset = False
        elif player == "O":
            self.displayed_player = self.player_o
        else:
            self.displayed_player = self.player_x

        self.surface.fill(self.background_color)
        self.message_surface.fill(self.display_color)
        self.message_surface.blit(self.displayed_player, (65, 0))
        self.message_surface.blit(self.message_text, (33, 40))

    def draw_menu(self, screen):
        self.surface.blit(self.message_surface, (158,5))
        self.surface.blit(self.reset_surface, self.reset_box.topleft)
        screen.blit(self.surface, self.box.topleft)