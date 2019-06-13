# -*- coding: utf-8 -*-
"""Basic CLI Dork.
"""
import sys
import os


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
    play_options = ('play', 'load', 'help', 'quit')
    option = ''
    while option not in play_options:
        option = input("> ").lower()
        if option == ("play"):
            setup_game()
        elif option == ("load"):
            load_game()
        elif option == ("help"):
            help_menu()
        elif option == ("quit"):
            end_game()
        else:
            print("Please enter a valid command.\n")


def title_screen():
    """Will display the title screen
    """
    os.system('cls')
    print("##########################")
    print("#   Welcome to the game  #")
    print("# Created by Team NoName #")
    print("##########################\n")
    print("          play            ")
    print("          load            ")
    print("          help            ")
    print("          quit            ")
    title_screen_selections()


def setup_game():
    """This will set up the game
    """
    os.system('cls')
    print("This will set the game up " +
          "and exicute the main loop for the game")


def help_menu():
    """Shows the help menu
    """
    os.system('cls')
    print("Help Menu")
    print("Movement: use 'move' and a direction")
    print("for example, move north, will move the character north if possible")
    print("Examine: you can examine rooms using 'examine' or 'look'")
    print("Items: some rooms have items that you might need further in")
    print("to pick up the item use the command 'pick up' or 'loot'\n")
    print("To return to title screen press enter.")
    option = input("> ").lower()
    if option == option:
        title_screen()


def load_game():
    """Will load a saved game
    """
    os.system('cls')
    print("This function is not currently in use.")
    print("This will eventually allow you to load a saved game.\n")
    print("To return to title screen press enter.")
    option = input("> ").lower()
    if option == option:
        title_screen()


def end_game():
    """Will show a end game screen and thank the player
    """
    os.system('cls')
    print("Thank you for playing")
    sys.exit()


title_screen()
