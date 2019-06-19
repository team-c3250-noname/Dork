"""Basic CLI Dork.
"""

import argparse
import os
import re
from io import StringIO
import cursor
import dork


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
    # print_help_then_exit = (True, True)
    # exit_only = (True, False)
    # run_dork = (False, False)
    dork_flags = (False, False)
    parser = argparse.ArgumentParser(description="Dork command line " +
                                     "interface. Run dork with no options to" +
                                     " begin game")

    parser.add_argument('-l', '--list', action='store_true',
                        help='list available mazes')
    parser.add_argument('-i', '--init',
                        help='-i <mazename> initializes dork with mazename')
    parser.add_argument('-o', '--out',
                        help='-o <mazename> generates a maze and saves it')
    parser.add_argument('-v', '--version', action='store_true',
                        help="prints version and exits")
    arglist = None
    unknown_args = None
    _hf = StringIO()
    parser.print_help(file=_hf)
    help_msg.append(_hf.getvalue())
    _hf.close()

    if "-h" in args or "--help" in args:
        return (True, True)

    try:
        arglist, unknown_args = parser.parse_known_args(args[1:])
        if unknown_args:
            print("Unrecognized command "+"".join(unknown_args))
            raise SystemExit
    except SystemExit:
        return (True, True)

    if arglist.out:
        if not is_filename_compliant(arglist.out):
            return (True, False)

        _f = open(__EXTENSION__[1:]+"/"+arglist.out+__EXTENSION__, "w")
        cursor.hide()
        dots = ("Generating maze    ", "Generating maze .",
                "Generating maze ..", "Generating maze ...")
        for _t in range(20):
            print("{}".format(dots[_t % 4]), end="\r")
        print(" "*len(dots[-1]))
        cursor.show()
        print("Done, maze \""+arglist.out+"\" saved")
        _f.close()

    if arglist.version:
        print(dork.__version__)
        dork_flags = (True, False)

    if arglist.list or arglist.init:
        mazes = []
        for (_, _, filenames) in os.walk(__EXTENSION__[1:]):
            mazes.extend(filenames)
        only_maze_files = [maze for maze in mazes
                           if maze.find(__EXTENSION__) > 0]
        if arglist.list:
            print(os.linesep.join(only_maze_files))
            dork_flags = (True, False)
        if arglist.init and arglist.init + __EXTENSION__ in only_maze_files:
            print("loaded maze "+arglist.init)
        elif arglist.init:
            print("maze "+arglist.init+" does not exist")
            return (True, True)

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
    prompt()


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


def prompt():
    """ Asks user what they would like to do
    """
    print("\n" + "What would you like to do?")
    acceptable_actions = ['move', 'go', 'walk', 'travel', 'quit',
                          'examine', 'inspect', 'look']
    d_action = list(zip(['examine', 'inspect', 'interact', 'look', 'pick up'],
                        [(player_examine, lambda x: [x])] * 5))
    da_action = list(zip(['move', 'go', 'travel', 'walk'],
                         [(player_move, lambda x: [x])]*4))
    daq_action = ("quit", (end_game, lambda x: []))

    d_action.extend(da_action)
    d_action.append(daq_action)

    commands = dict(d_action)
    action = ""
    check = True
    while check:
        action = input("> ").lower()
        user_action = action.split()
        mycommand = [(x in acceptable_actions, x) for x in user_action]
        if mycommand:
            args = commands[mycommand[0][1]][1](user_action)
            check = commands[mycommand[0][1]][0](*args)
            if not check:
                break
        check = any(x in acceptable_actions for x in user_action)


def player_move(user_action):
    """ Allows player to move along maze
    """
    if 'north' in user_action:
        print("This will take you north")
        prompt()
    elif 'south' in user_action:
        print('This will take you south')
        prompt()
    elif 'west' in user_action:
        print('This will take you west')
        prompt()
    elif 'east' in user_action:
        print('This will take you east')
        prompt()


def player_examine(user_action):
    """ Allows player to interact with things in room
    """
    if user_action in ['examine', 'inspect']:
        print("Item description")
    elif user_action in ['interact']:
        print('You interacted with item')
    elif user_action in ['pickup']:
        print('The item is in your hand')
