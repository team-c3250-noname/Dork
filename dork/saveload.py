"""Save and load system for dork
"""
# Generously inspired by our LA,
# https://github.com/LSmith-Zenoscave

import yaml
import dork.types as types


def get_input():
    """
    Reads user input to create a file name for use in save/load.
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
    When called, asks the user for a file name and loads it to the game state.
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
        OSError: If the file_name is invalid, such as when the player is on
        Windows and attempts to name the file '?'.
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
        except (OSError, FileNotFoundError, ValueError):
            print("ERROR: Invalid file name: " + file_name)
            print("Please try a different file name.")
            file_name = get_input()

    print("")
    print("Load successful.")
    print("")

    return data


def save(game):
    """
    Save the game state into a yaml file by prompting for an input name.
    The save function starts by assigning to data the current game state,
    and then prompts the user with get_input() to input a save file name.
    It then enters two loops: the first one ensures that the save name does
    not contain 'default' as that is our base game that we do not want to
    overwrite. The second loop ensures that the filename is valid and does
    not produce any errors, and will continue to prompt the user for a new
    filename until they input a valid one. Once we have a valid filename,
    we use yaml's safe_dump() function to dump the data into a dictionary.
    Finally, we return 0 to indicate a successful execution of save().

    Args:
        game: A dictionary containing the current game state.

    Returns:
        0: If the function successfully executes, returns a 0 to indicate
        that success.

    Raises:
        OSError: If the user is on Windows and attempts to use a forbidden
        character, such as '?', for the file name.
        ValueError: If the user inputs an invalid file name, such as a null
        terminator.
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
    """
    First, data is loaded using load() and then returned as a game sate.
    This function starts by assigning to data using load(), and then
    immediately returns the game state.

    Returns:
        types.Game(data): A dictionary containing the game state.
    """
    data = load()
    return types.Game(data)
