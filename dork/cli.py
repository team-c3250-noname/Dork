"""Basic CLI Dork.
"""

import argparse
import os
import re
from io import StringIO
import cursor
import dork
import dork.saveload


__all__ = ["main"]

__EXTENSION__ = ".yml"


def is_filename_compliant(filename):
    """checks if filename follows win and unix naming guidelines
       https://docs.microsoft.com/en-us/windows/desktop/FileIO/naming-a-file
       added in NULL character as well
    """
    if re.match(r'<|>|:|"|\/|\\|\||\?|\*|\0', filename):
        print(r"filenames cannot contain <, >, :, /, \|, ?, *")
        return False
    match = r'^((CON)|(PRN)|(AUX)|(NUL)|(COM)\d{1}|(LPT)\d{1})\.*(\w{3})*$'
    if re.match(match, filename):
        print("Filename cannot be a OS reserved name")
        return False
    if re.match(r'^.*( |\.)$', filename):
        print("Filenames should not end with space or period")
        return False
    return True


def the_predork_cli(help_msg, *args):
    """non-game loop command line """

    def _out(filename):
        if not is_filename_compliant(filename):
            return (True, False)

        _f = open(__EXTENSION__[1:] + "/" + filename + __EXTENSION__, "w")
        cursor.hide()
        dots = ("Generating maze    ", "Generating maze .",
                "Generating maze ..", "Generating maze ...")
        for _t in range(20):
            print("{}".format(dots[_t % 4]), end="\r")
        print(" "*len(dots[-1]))
        cursor.show()
        print("Done, maze \"" + filename + "\" saved")
        _f.close()
        return (True, False)

    def no_arg(arg):
        arg = arg
        return []

    def one_arg(arg):
        return [arg]

    def _version():
        print(dork.__version__)
        return (True, False)

    def _list():
        print(os.linesep.join(get_maze_files()))
        return (True, False)

    def get_maze_files():
        mazes = []
        for (_, _, filenames) in os.walk(__EXTENSION__[1:]):
            mazes.extend(filenames)
        return [maze for maze in mazes
                if maze.find(__EXTENSION__) > 0]

    def _init(filename):
        if filename and filename + __EXTENSION__ in get_maze_files():
            print("loaded maze " + filename)
            return (False, False)
        print("maze " + filename + " does not exist")
        return (True, False)

    dork_flags = (True, True)
    parser = argparse.ArgumentParser(description="Dork command line " +
                                     "interface. Run dork with no options to" +
                                     " begin game", add_help=False)

    parser.add_argument('-l', '--list', action='store_true',
                        help='list available mazes')
    parser.add_argument('-i', '--init',
                        help='-i <mazename> initializes dork with mazename')
    parser.add_argument('-o', '--out',
                        help='-o <mazename> generates a maze and saves it')
    parser.add_argument('-v', '--version', action='store_true',
                        help="prints version and exits")

    _hf = StringIO()
    parser.print_help(file=_hf)
    help_msg.append(_hf.getvalue())
    _hf.close()
    arglist, _ = parser.parse_known_args(args[1:])

    options = {"out": one_arg, "init": one_arg,
               "version": no_arg, "list": no_arg}
    for option in options:
        if arglist and option in arglist.__dict__ and arglist.__dict__[option]:
            args = options[option](arglist.__dict__[option])
            dork_flags = locals()["_"+option](*args)

    return dork_flags


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
    play_options = {'play': setup_game, 'load': load_game,
                    'help': help_menu, 'quit': end_game}
    user_play = True
    print("##########################")
    print("#   Welcome to the game  #")
    print("# Created by Team NoName #")
    print("##########################")
    print("")
    print("          play            ")
    print("          load            ")
    print("          help            ")
    print("          quit            ")
    while user_play is True:
        option = input("> ")
        if option in play_options:
            user_play = play_options[option]()
        else:
            print("Please enter a valid command.\n")


def setup_game():
    """This will set up the game
    """
    print("This will set the game up " +
          "and execute the main loop for the game")
    prompt()


def help_menu():
    """Shows the help menu
    """
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
    dork.saveload.main()


def end_game():
    """Will show a end game screen and thank the player
    """
    print("Thank you for playing")
    return False


def prompt():
    """ Asks user what they would like to do
    """
    keep_prompting = True

    def one_arg(args):
        return [args]

    def no_arg(args):
        args = args
        return []

    player_actions = {'move': (player_move, one_arg),
                      'go': (player_move, one_arg),
                      'walk': (player_move, one_arg),
                      'examine': (player_examine, one_arg),
                      'look': (player_examine, one_arg),
                      'quit': (end_game, no_arg)}
    while keep_prompting is True:
        user_action = input("\n" + "What would you like to do? ").split()
        action = next((word for word in user_action if word in player_actions),
                      '')
        if action in player_actions:
            args = player_actions[action][1](user_action)
            keep_prompting = player_actions[action][0](*args)
        else:
            print("Enter a valid command. ")


def player_move(user_action):
    """ Allows player to move along maze
    """
    if 'north' in user_action:
        print("This will take you north")
    elif 'south' in user_action:
        print('This will take you south')
    elif 'west' in user_action:
        print('This will take you west')
    elif 'east' in user_action:
        print('This will take you east')
    else:
        print("Invalid direction")
    return True


def player_examine(user_action):
    """ Allows users to examine the room and items
    """
    if 'room' in user_action:
        print("This is a room")
    else:
        print("This will examine the item or room")
    return True
