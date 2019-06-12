import sys

# -*- coding: utf-8 -*-
"""Basic CLI Dork.
"""

__all__ = ["main"]


def main(*args):
    """Main CLI runner for Dork
    """
    script_name = args[0] if args else '???'
    if "-h" in args or '--help' in args:
        print("usage:", script_name, "[-h]")
    else:
        print(*args)



class Player():

    """Creates the player
    """
    def __init__(self):
        self.game_over = False
MY_PLAYER = Player()


def title_screen_selections():
    """Will allow the user to choose what to do
    """
    option = input("> ")

    if option.lower() == ("play"):
        setup_game()
    elif option.lower() == ("help"):
        help_menu()
    elif option.lower() == ("load"):
        load_game()
    elif option.lower() == ("quit"):
        print("Thank you for playing the game.")
        sys.exit()

    while option.lower() not in ['play', 'load', 'help', 'quit']:
        print("Please enter a valid command.")
        option = input("> ")
        if option.lower() == ("play"):
            setup_game()
        elif option.lower() == ("load"):
            load_game()
        elif option.lower() == ("help"):
            help_menu()
        elif option.lower() == ("quit"):
            print("Thank you for playing the game.")
            sys.exit()


def title_screen():
    """Will display the title screen
    """
    print("Welcome to the game")
    print("Created by Team NoName\n")
    print("play")
    print("load")
    print("help")
    print("quit")
    title_screen_selections()


def help_menu():
    """Shows the help menu
    """
    print("Help Menu")
    print("Movement: use 'move' and a direction")
    print("for example, move north, will move the character north if possible")
    print("Examine: you can examine rooms using 'examine' or 'look'")
    print("Items: some rooms have items that you might need further in")
    print("to pick up the item use the command 'pick up' or 'loot'\n")
    title_screen_selections()


def setup_game():
    """This will set up the game
    """
    print("This will set the game up " +
          "and exicute the main loop for the game")


def load_game():
    """Will load a saved game
    """
    print("This function is not currently in use.")
    print("This will eventually allow you to load a saved game.\n")
    title_screen_selections()



title_screen()
