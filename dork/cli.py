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

#interaction

def prompt():
    """ Asks user what they would like to do
    """
    print("\n" + "What would you like to do?")
    action = input("> ")
    acceptable_actions = ['move', 'go', 'walk', 'travel', 'quit', 'examine', 'inspect', 'look']
    while action.lower() not in acceptable_actions:
        print ("Unknown action, try again.\n")
        if action.lower == 'quit':
            sys.exit()
        elif action.lower() in ['move', 'go', 'travel', 'walk']:
            player_move(action.lower())
        elif action.lower() in ['examine', 'inspect', 'interact', 'look', 'pick up']:
            player_examine(action.lower())


def player_move(action):
    if action.lower() in ['north']:
        print("This will take you north")
    elif action.lower() in ['south']:
        print('This will take you south')
    elif action.lower() in ['west']:
        print('This will take you west')
    elif action.lower() in ['east']:
        print('This will take you east')


def player_examine(action):
    if action.lower() in ['examine', 'inspect']:
        print("Item description")
    elif action.lower() in ['interact']:
        print()
    elif action.lower() in ['pickup']:
        print('The item is in your hand')
