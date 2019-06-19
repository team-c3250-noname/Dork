# -*- coding: utf-8 -*-
"""Basic CLI Dork.
"""
import os


__all__ = ["main"]


def main(*args):
    """Main CLI runner for Dork
    """
    help_msg = []

    exit_dork, print_help = the_predork_cli(help_msg, *args)

    if print_help:
        print(help_msg[0])
    if exit_dork:
        return

    print("running dork")
    title_screen()


def title_screen():
    """Will display the title screen
    """
    os.system('cls')
    play_options = {'play': setup_game, 'load': load_game,
                    'help': help_menu, 'quit': end_game}
    user_play = True
    while user_play is True:
        os.system('cls')
        print("##########################")
        print("#   Welcome to the game  #")
        print("# Created by Team NoName #")
        print("##########################")
        print("")
        print("          play            ")
        print("          load            ")
        print("          help            ")
        print("          quit            ")
        option = input("> ")
        if option in play_options:
            user_play = play_options[option]()
        else:
            print("Please enter a valid command.\n")


def setup_game():
    """This will set up the game
    """
    os.system('cls')
    print("This will set the game up " +
          "and execute the main loop for the game")
    input("To return to title screen press enter.")
    return True


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
    input("To return to title screen press enter.")
    return True


def load_game():
    """Will load a saved game
    """
    os.system('cls')
    print("This function is not currently in use.")
    print("This will eventually allow you to load a saved game.\n")
    input("To return to title screen press enter.")
    return True


def end_game():
    """Will show a end game screen and thank the player
    """
    os.system('cls')
    print("Thank you for playing")
    return False
