"""Save and load system for dork
"""
# Generously inspired by our LA,
# https://github.com/LSmith-Zenoscave

import yaml
from dork import cli


def get_input():
    """Grabs user input to define a save/load name
    """
    input_name = input("Enter a file name: ")
    file_name = "./dork/yaml/" + input_name + ".yml"

    return file_name


def load():
    """This will load a file into data.
    """
    print("Attempting to load data.")

    file_name = get_input()
    loaded = False

    while loaded is False:
        try:
            with open(file_name) as file:
                data = yaml.safe_load(file.read())
                loaded = True
        except IOError:
            print("ERROR: Invalid file name: " + file_name)
            print("Please try a different file name.")
            file_name = get_input()

    print("Load successful.")

    return data


def save(data):
    """This will save player and room data to a file.
    Eventually this should also save maze data.
    """
    print("Attempting to save data.")

    file_name = get_input()
    saved = False

    while saved is False:
        try:
            with open(file_name, 'w') as yaml_file:
                yaml.safe_dump(data, default_flow_style=False,
                               stream=yaml_file)
                saved = True
        except IOError:
            print("ERROR: Invalid file name: " + file_name)
            print("Please try a different file name.")
            file_name = get_input()

    print("Save successful.")
    return 0


def main():
    """Runs everything.
    """
    game = cli.game_state()
    save(game.save())


if __name__ == "__main__":
    main()
