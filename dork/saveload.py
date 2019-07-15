"""Save and load system for dork
"""
# Generously inspired by our LA,
# https://github.com/LSmith-Zenoscave

import sys
import yaml
from dork import cli


PROPERTIES = ["Items", "Player", "Rooms"]
PLAYERDATA = ["holding", "location", "current", "max"]
ITEMDATA = ["holds"]
DIRECTIONS = ["north", "south", "east", "west"]


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

    try:
        with open(file_name) as file:
            data = yaml.safe_load(file.read())
    except IOError:
        sys.exit("ERROR: Invalid file name: " +
                 file_name + ". Exiting program.")

    print("Load successful.")
    print("")

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


def pplayer(players, name, pdata):
    """Parses player data into useful info.
    """
    player = players[name]
    if pdata not in player:
        pass
    elif player[pdata] is None:
        print(f"There is no data in {name}.")
    else:
        other = player[pdata]
        print(f"Player {pdata} {name}: {other}.")


def pitem(items, name, idata):
    """Parses item data into useful info.
    """
    item = items[name]
    if idata not in item:
        print(f"{name} does not have {idata} as a key.")
    elif item[idata] is None:
        print(f"There are no items in {name}.")
    else:
        other = item[idata]
        print(f"{other} is in {name}.")


def path(rooms, name, direction):
    """Parses room information into useful data.
    """
    room = rooms[name]
    if direction not in room:
        print(f"{name} does not have {direction} as a key.")
    elif room[direction] is None:
        print(f"There is nothing {direction} of {name}.")
    elif room[direction] not in rooms:
        print(f"Going {direction} from {name} will lead to an error.")
    else:
        other = room[direction]
        print(f"{other} is {direction} of {name}.")


def main():  # pragma: no cover
    """Runs everything.
    """
    game = cli.game_state()
    # print("Data that was loaded:")
    # pprint(data)

    # print("Checking rooms, items, and player data for errors...")
    # for ppty in PROPERTIES:
    #    if ppty not in data:
    #        print(f"No {ppty} found.")
    #    if not isinstance(data[ppty], dict):
    #        print(f"{ppty} in data were not proper data.")
    #        return

    # parseroom(data)
    # parseitem(data)
    # parseplayer(data)
    save(game.save())


def parseroom(roomdata):
    """Parses room data.
    """
    rooms = roomdata["Rooms"]
    for name in rooms:
        for direction in DIRECTIONS:
            path(rooms, name, direction)


def parseitem(roomdata):
    """Parses item data.
    """
    items = roomdata["Items"]
    for name in items:
        for idata in ITEMDATA:
            pitem(items, name, idata)


def parseplayer(roomdata):
    """Parses player data.
    """
    players = roomdata["Player"]
    for name in players:
        for pdata in PLAYERDATA:
            pplayer(players, name, pdata)


if __name__ == "__main__":  # pragma: no cover
    main()
