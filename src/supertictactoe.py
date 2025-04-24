import terminalFunctions as game

def main():
    while True:
        game.game_loop()
        while True:
            option = input("Play again? (Y/N): ").capitalize()
            if option != "Y" and option != "N":
                print("enter a valid input")
                continue
            break
        if option == "N":
            print("Thanks for playing!")
            break



if __name__ == "__main__":
    main()