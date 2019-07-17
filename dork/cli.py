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
    player_room_description = game.rooms[player.position['location']].messages[
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
    print("the player is in the " + player.position['location'])
    print(game.rooms[player.position['location']].messages['description'])
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
    keep_prompting = True
    not_last = False
    dead = False

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
                      'quit': (end_game, no_arg),
                      'checkscore': (check_score, no_arg) }
    while keep_prompting is True and not_last is False and dead is False:
        user_action = input("\n" +
                            "What would you like to do? ").lower().split()
        action = next((word for word in user_action if word in player_actions),
                      '')
        if action in player_actions:
            args = player_actions[action][1](user_action)
            keep_prompting = player_actions[action][0](game, *args)
            dead = fight_check(game)
            not_last = last_room(game)
        else:
            print("Enter a valid command. ")


def last_room(game):
    """Will check if its the last room
    """
    player = game.player
    if player.position['location'] == player.position['last room']:
        return True
    return False


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
        lock_check(game, game.rooms[player.position[
            'location']].paths[cardinal])
    else:
        print("Invalid direction")
    return True


def lock_check(game, direction):
    """This will check if the door is locked
    """
    player = game.player
    if direction != '':
        player.position['next location'] = direction
        next_lock = game.rooms[player.position['next location']].door['locked']
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
    player.position['location'] = destination
    print("You have moved to " + destination)
    print("")
    print(game.rooms[player.position['location']].messages['description'])


def player_examine(game, user_action):
    """ Allows users to examine the room and items
    """
    player = game.player
    item = next((word for word in user_action if word in player.inventory), '')
    if 'room' in user_action:
        room_examine(game)
    elif item in user_action:
        print(game.items[item].description)
    else:
        print("You are trying to examine an unknown thing. Please try again")
    return True


def room_examine(game):
    """Will examine the room
    """
    player = game.player
    if game.rooms[player.position['location']].door['item'] != []:
        print(game.rooms[player.position['location']].messages['inspect'])
        print("This room contains:")
        print(game.rooms[player.position['location']].door['item'])
    else:
        print("There is nothing useful here.")


def player_take(game, user_action):
    """Allows user to pick up items and puts them in the players inventory
    """
    player = game.player
    item = game.rooms[player.position['location']].door['item']
    key_word = next((word for word in user_action if word in item), 'item')
    if key_word in item:
        print("You have picked up the " + key_word)
        player.inventory.append(key_word)
        game.rooms[player.position['location']].door['item'].remove(key_word)
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
    player.position['next location'] = direction
    unlock = room_check(game, direction)
    if unlock == '':
        print("You dont think that will work.")
    else:
        unlock = unlock.split()
        key_word = next((word for word in user_action if word in unlock),
                        'item')
        if key_word in unlock:
            unlock_message = game.rooms[player.position[
                'next location']].messages['unlock message']
            game.rooms[player.position['next location']].door['locked'] = False
            print(unlock_message)
            remove_item(game)
        else:
            print('You do not have the key for this room.')


def remove_item(game):
    """Removes item after being used from inventory
    """
    player = game.player
    item = game.rooms[player.position['next location']].door['unlock']
    player.inventory.remove(item)


def drop_item(game):
    """Returns item to room from inventory
    """
    player = game.player
    print(player.inventory)
    if player.inventory == []:
        print("You have no items to drop.")
        return True
    item = input('What would you like to drop?')
    if item not in player.inventory:
        print("That isn't an item you have.")
        return True
    game.rooms[player.position['location']].door['item'].append(item)
    player.inventory.remove(item)
    return True


def room_check(game, direction):
    """This will check if the room exists
    """
    player = game.player
    if direction != '':
        return game.rooms[player.position['next location']].door['unlock']
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
            return game.rooms[player.position['location']].paths[direction]
        direction_check = input("Please input cardinal direction. ").lower()


def fight_check(game):
    """Will check if the user has an enemy to fight
    """
    check = False
    player = game.player
    if game.rooms[player.position['location']].fight['fight'] is True:
        check = fight_prompt(game)
    return check


def fight_prompt(game):
    """Fighting enemy
    """
    player = game.player
    enemy = game.rooms[player.position['location']].fight['enemy']
    flag = True
    print('You have encountered a ' + enemy)
    while flag is True:
        action = input('Do you want to punch or swing? ')
        if 'punch' in action:
            flag = False
            damage = player.stats['attack']
            check2 = fight(game, enemy, damage)
        elif 'swing' in action:
            flag = False
            if player.inventory == []:
                damage = player.stats['attack']
                print('You have nothing so fight like a man')
            else:
                print('what item do you want to use.')
                print(player.inventory)
                item = input()
                while item not in player.inventory:
                    print('Dont you wish you had ' + item)
                    item = input('Try again: ')
                damage = game.items[item].damage
            check2 = fight(game, enemy, damage)
        else:
            print('invalid command')
    return check2


def fight(game, enemy, damage):
    """Basic fight
    """
    player = game.player
    ehealth = game.npc[enemy].health
    fighting = True

    while fighting is True:
        print('Your health is ' + str(player.stats['health']))
        ehealth -= damage
        print('You have damaged the ' + enemy + ' for ' + str(damage))
        if ehealth <= 0:
            print("You have killed the " + enemy)
            if 'guard' in enemy:
                player.stats['point'] += 10
                print('You have gain 10 points')
            elif 'boss' in enemy:
                player.stats['point'] += 100
                print('You have gain 100 points')
            game.rooms[player.position['location']].fight['fight'] = False
            fighting = False
            flag = False
            break
        player.stats['health'] -= game.npc[enemy].attack
        print('You take ' + str(game.npc[enemy].attack))
        if player.stats['health'] <= 0:
            print('You have died')
            fighting = False
            flag = True
    return flag

def check_score(game):
    """Check current score
    """
    player = game.player
    score = player.stats['point']
    print(f"Your current score is: {score}")
    return True