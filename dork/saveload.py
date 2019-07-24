"""Save and load system for dork
"""
# Generously inspired by our LA,
# https://github.com/LSmith-Zenoscave

import yaml
import dork.types as types


def get_input():
    """
    Summary:
        Reads user input to create a file name for use in save/load.

    Description:
        This function is intended to grab user input for use in file_name.
        It uses the input() method to first get a file name, before appending
        ./dork/yaml/ at the front and .yml in the back. Finally, it returns
        the completed file_name for use in creating save files or looking
        for a file to load in other methods.

    Note:
        input_name cannot contain "default" within it when saving a file
        as it is a protected name for our default save.

    Returns:
        file_name: A string containing a file path for use in save/load ops.
    """
    input_name = input("Enter a file name: ")
    file_name = "./dork/yaml/" + input_name + ".yml"

    return file_name


def load():
    """
    Summary:
        When called, asks the user for a file name, and then loads it into
        the game state.

    Description:
        This function starts by calling get_input() to receive a file name
        from the player and then enters a loop where it checks for the validity
        of the given file name. If we have no errors it uses yaml's safe_load()
        function to load the .yml dictionary into the data to be used for the
        game state. If we do have any errors, we ask the user for a different
        file name until they give us one that is valid, whereupon the loaded
        flag is set to True and we exit the loop. Finally, it returns the data.

    Returns:
        data: A dictionary containing game state information such as player
        location and inventory, rooms and their connections/items, NPCs, etc.

    Raises:
        IOError: This one should be rare (in cases where the disk is full),
        and is here primarily for safety.
        FileNotFoundError: If the file_name doesn't exist as a .yml file yet.
        ValueError: If the file_name has something inappropriate in it, like
        a null terminator.
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


def save(game):
    """Save the game state into a yaml file.
    Also prompts the user for a file name.
    """
    print("Attempting to save data.")

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
    data = load()
    return types.Game(data)
