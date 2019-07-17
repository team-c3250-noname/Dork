"""Save and load system for dork
"""
# Generously inspired by our LA,
# https://github.com/LSmith-Zenoscave

import yaml
import dork.types as types


def get_input():
    """Grabs user input to define a save/load name
    """
    input_name = input("Enter a file name: ")
    file_name = "./dork/yaml/" + input_name + ".yml"

    return file_name


def load():
    """Load a yaml file, returning it as data.
    The user is prompted for a file name.
    """
    print("Attempting to load data.")

    file_name = get_input()
    loaded = False

    while loaded is False:
        try:
            with open(file_name) as file:
                data = yaml.safe_load(file.read())
                loaded = True
        except (IOError, FileNotFoundError, ValueError):
            print("ERROR: Invalid file name: " + file_name)
            print("Please try a different file name.")
            file_name = get_input()

    print("")
    print("Load successful.")
    print("")

    return data


def save():
    """Save the game state into a yaml file.
    Also prompts the user for a file name.
    """
    print("Attempting to save data.")

    game = game_state()
    data = game.save()
    file_name = get_input()
    saved = False
    name_ok = False

    while name_ok is False:
        if 'default' in file_name:
            print("You cannot use this name. Pick another.")
            file_name = get_input()
        else:
            name_ok = True

    while saved is False:
        try:
            with open(file_name, 'w') as yaml_file:
                yaml.safe_dump(data, default_flow_style=False,
                               stream=yaml_file)
                saved = True
        except (IOError, ValueError):
            print("ERROR: Invalid file name: " + file_name)
            print("Please try a different file name.")
            file_name = get_input()

    print("")
    print("Save successful.")
    print("")

    return 0


def game_state():
    """Creates and stores the game state.
    """
    if types.GAME is None:
        data = load()
        types.GAME = types.Game(data)
    return types.GAME
