"""Basic CLI Dork.
"""

import argparse
import os
import re
from io import StringIO
import cursor
import dork
import dork.saveload as sl


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


def get_help_message(argparser):
    """gets help message from argparser
    """
    help_msg_file = StringIO()
    argparser.print_help(file=help_msg_file)
    msg = help_msg_file.getvalue()
    help_msg_file.close()
    return msg


def the_predork_cli(help_msg, *args):
    """non-game loop command line """
    if len(args) < 2:
        return (False, False)

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

    def _no_arg(_args):
        return []

    def _one_arg(arg):
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

    help_msg.append(get_help_message(parser))

    arglist, _ = parser.parse_known_args(args[1:])

    options = {"out": _one_arg, "init": _one_arg,
               "version": _no_arg, "list": _no_arg}
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
                    'help': help_menu, 'quit': quit_game}
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
        option = input("> ").strip()
        if option in play_options:
            user_play = play_options[option]()
        else:
            print("Please enter a valid command.\n")


def setup_game():
    """This will set up the game
    """
    game = sl.game_state()
    player = game.player
    player_room_description = game.rooms[player.location].messages[
        'description']
    print(player_room_description)
    prompt()


def help_menu():
    """Shows the help menu
    """
    print("                            Help Menu")
    print("""
    Movement: To move use simple commands you can say walk or
    move and a direction. i.e. 'move north' or 'go south'.

    Examine: To examine the area around you use the keyword
    examine or inspect and what ever you want to inspect.
    i.e. to look at the room use 'inspect room'.

    Items: Some rooms will have items that you can pick up.
    Use the keyword 'pick' to put an item into your inventory.
    i.e. 'pick up excaliber'.

    Help: If you need to be reminded of available actions
    while playing the game use the keyword 'help' to access
    the help menu.
    """)
    print("")
    input("To return press enter.")
    return True


def load_game():
    """Will load a saved game
    """
    game = sl.game_state()
    player = game.player
    print("the player is in the " + player.location)
    print(game.rooms[player.location].messages['description'])
    prompt()


def quit_game():
    """This will quit the game
    """
    print("Thank you for playing")
    return False


def end_game(_game):
    """Will show a end game screen and thank the player
    """
    print("Thank you for playing")
    return False


def prompt():
    """ Asks user what they would like to do
    """
    game = sl.game_state()
    player = game.player
    keep_prompting = True

    def one_arg(args):
        return [args]

    def no_arg(_args):
        return []

    player_actions = {'move': (player_move, one_arg),
                      'go': (player_move, one_arg),
                      'walk': (player_move, one_arg),
                      'examine': (player_examine, one_arg),
                      'inspect': (player_examine, one_arg),
                      'pick': (player_take, one_arg),
                      'take': (player_take, one_arg),
                      'use': (player_use, one_arg),
                      'drop': (drop_item, no_arg),
                      'user': (user_menu, one_arg),
                      'help': (help_menu, no_arg),
                      'save': (save_game, no_arg),
                      'quit': (end_game, no_arg), }
    while keep_prompting is True and player.location != player.last_room:
        user_action = input("\n" +
                            "What would you like to do? ").lower().split()
        action = next((word for word in user_action if word in player_actions),
                      '')
        if action in player_actions:
            args = player_actions[action][1](user_action)
            keep_prompting = player_actions[action][0](game, *args)
        else:
            print("Enter a valid command. ")


def save_game(_game):
    """Allows player to save the game
    """
    dork.saveload.save()


def player_move(game, user_action):
    """ Allows player to move along maze
    """
    player = game.player
    directions = ['north', 'up', 'south', 'down', 'east',
                  'left', 'west', 'right', ]
    action = next((word for word in user_action if word in directions), '')
    player_direction = {'north': 'up', 'up': 'up', 'south': 'down',
                        'down': 'down', 'east': 'right',
                        'right': 'right', 'west': 'left',
                        'left': 'left', }
    if action in player_direction:
        cardinal = player_direction[action]
        lock_check(game, game.rooms[player.location].paths[cardinal])
    else:
        print("Invalid direction")
    return True


def lock_check(game, direction):
    """This will check if the door is locked
    """
    player = game.player
    if direction != '':
        player.next_location = direction
        next_lock = game.rooms[player.next_location].door['locked']
        if next_lock is True:
            print("The door doesn't open.")
            print('You might be able to use an item.')
        else:
            movement_handler(game, direction)
    if direction == '':
        print("That is a wall")


def movement_handler(game, destination):
    """ This will handle movement to different rooms
    """
    player = game.player
    player.location = destination
    print("You have moved to " + destination)
    print("")
    print(game.rooms[player.location].messages['description'])


def player_examine(game, user_action):
    """ Allows users to examine the room and items
    """
    if 'room' in user_action:
        room_examine(game)
    else:
        print("You are trying to examine an unknown thing. Please try again")
    return True


def room_examine(game):
    """Will examine the room
    """
    player = game.player
    if game.rooms[player.location].door['item'] != '':
        print(game.rooms[player.location].messages['inspect'])
        print("This room contains a ")
        print(game.rooms[player.location].door['item'])
    else:
        print("There is nothing useful here. ")


def player_take(game, user_action):
    """Allows user to pick up items and puts them in the players inventory
    """
    player = game.player
    item = game.rooms[player.location].door['item']
    key_word = next((word for word in user_action if word in item), 'item')
    if key_word in item:
        print("You have picked up the " + key_word)
        player.inventory.append(key_word)
        game.rooms[player.location].door['item'].remove(key_word)
    else:
        print("There is no such item")
    return True


def user_menu(game, user_action):
    """Allows users to view their menu
    """
    player = game.player
    if 'inventory' in user_action:
        print(player.inventory)
    elif 'save' in user_action:
        print("This will lead to saving the game.")
    else:
        print("No menu option found")
    return True


def player_use(game, user_action):
    """Allows player to use items
    """
    player = game.player
    inventory = ' '.join(player.inventory)
    key_word = next((word for word in user_action if word in inventory),
                    'item')
    if key_word in inventory:
        direction = next_room(game)
        unlock_room(game, user_action, direction)
    else:
        print("You do not have that item.")
    return True


def unlock_room(game, user_action, direction):
    """unlocks room
    """
    player = game.player
    player.next_location = direction
    unlock = room_check(game, direction)
    if unlock == '':
        print("You dont think that will work.")
    else:
        unlock = unlock.split()
        key_word = next((word for word in user_action if word in unlock),
                        'item')
        if key_word in unlock:
            unlock_message = game.rooms[player.next_location].messages[
                'unlock message']
            game.rooms[player.next_location].door['locked'] = False
            print(unlock_message)
            remove_item(game)
        else:
            print('You do not have the key for this room.')


def remove_item(game):
    """Removes item after being used from inventory
    """
    player = game.player
    item = game.rooms[player.next_location].door['unlock']
    player.inventory.remove(item)


def drop_item(game):
    """Returns item to room from inventory
    """
    player = game.player
    print(player.inventory)
    item = input('What would you like to drop?')
    game.rooms[player.location].door['item'] += item
    player.inventory.remove(item)
    return True


def room_check(game, direction):
    """This will check if the room exists
    """
    player = game.player
    if direction != '':
        return game.rooms[player.next_location].door['unlock']
    return ''


def next_room(game):
    """Will find the rooms next to the player
    """
    player = game.player
    player_directions = {'north': 'up', 'up': 'up',
                         'south': 'down', 'down': 'down',
                         'east': 'right', 'right': 'right',
                         'west': 'left', 'left': 'left', }
    direction_check = input("Which direction would you like to try ").lower()
    reprompt = True
    while reprompt is True:
        if direction_check in player_directions:
            direction = player_directions[direction_check]
            reprompt = False
            return game.rooms[player.location].paths[direction]
        direction_check = input("Please input cardinal direction. ").lower()
