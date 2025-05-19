import terminalFunctions as game
import pygame as pg
import os
import uiFunctions

def terminal():
    while True:
        game.super_game_loop_terminal()
        while True:
            option = input("Play again? (Y/N): ").capitalize()
            if option != "Y" and option != "N":
                print("enter a valid input")
                continue
            break
        if option == "N":
            print("Thanks for playing!")
            break

def main():
    game_data = uiFunctions.GameUI()
    pg.init()
    screen = pg.display.set_mode((474, 640))
    clock = pg.time.Clock()
    running = True

    #input loop
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            #checking if mouse was clicked
            if event.type == pg.MOUSEBUTTONUP:
                #update the board with the mouse position
                game_data.update_game_state(event.pos)

        #render the game
        screen.fill([0,0,0])
        game_data.draw_game(screen)

        pg.display.flip()
        clock.tick(60)
    pg.quit()


def test_board():

    # pygame setup
    pg.init()
    screen = pg.display.set_mode((474, 640))
    clock = pg.time.Clock()
    running = True

    #all of these can be made variables of the super board class
    #surface to make the super_board
    game_surface = pg.surface.Surface([474, 474])
    #width of the lines on the super_board
    LINE_WIDTH = 9
    #the size (width and height its a square) of each little board
    BOARD_SIZE = 152

    #a list of surfaces, used for both collision detection
    #make this a variable of the super board class
    boards_surface = []
    for i in range(3):
        for j in range(3):
            boards_surface.append([[255, 255, 255], pg.rect.Rect(i * (LINE_WIDTH + BOARD_SIZE), j * (LINE_WIDTH + BOARD_SIZE), BOARD_SIZE, BOARD_SIZE)])

    #Just a bunch of color constants
    BLACK = [0,0,0]
    WHITE = [255,255,255]
    RED = [255, 34, 0]
    BLUE = [0, 60, 255]

    #the loop to check for board interactions
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            #checking if mouse was clicked
            if event.type == pg.MOUSEBUTTONUP:

                #checking each little board to see if it was clicked
                #make this a function
                for rec in boards_surface:
                    if rec[1].collidepoint(event.pos):

                        #changing the state of the board
                        #make this a function
                        if rec[0] == WHITE:
                            rec[0] = [0, 255, 234]
                        else:
                            rec[0] = WHITE

        # fill the screen with a color to wipe away anything from last frame
        screen.fill([30, 255, 0])
        game_surface.fill(BLACK)

        # RENDER YOUR GAME HERE

        #test = pg.image.load(os.path.join('files', 'SuperTicTacToeBoard.png')).convert()
        #test.set_colorkey([255,255,255])
        #screen.blit(test, [0,0])0
        '''
        pg.draw.line(game_surface, [0,0,0], [game_surface.get_width() / 3, 0], [game_surface.get_width() / 3, game_surface.get_height()], 10)
        pg.draw.line(game_surface, [0,0,0], [2 * game_surface.get_width() / 3, 0], [2 * game_surface.get_width() / 3, game_surface.get_height()], 10)
        pg.draw.line(game_surface, [0,0,0], [0, game_surface.get_height() / 3], [game_surface.get_width(), game_surface.get_height() / 3], 10)
        pg.draw.line(game_surface, [0,0,0], [0, 2 * game_surface.get_height() / 3], [game_surface.get_width(), 2 * game_surface.get_height() / 3], 10)
        screen.blit(game_surface, [0,0])
        '''

        #make this a function:
        # only needs to take in the game surface, you can make that a variable of the superboard class
        for rec in boards_surface:
            pg.draw.rect(game_surface, rec[0], rec[1])
            if rec[0] != WHITE:
                pg.draw.line(game_surface, RED, rec[1].topleft, rec[1].bottomright, 5)
                pg.draw.line(game_surface, RED, rec[1].topright, rec[1].bottomleft, 5)


        screen.blit(game_surface, [0,0])
        # flip() the display to put your work on screen
        pg.display.flip()

        clock.tick(60)  # limits FPS to 60

    pg.quit()

if __name__ == "__main__":
    main()