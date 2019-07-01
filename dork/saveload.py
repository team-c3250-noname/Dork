"""Save and load system for dork
"""
# Generously inspired by our LA,
# https://github.com/LSmith-Zenoscave

from pprint import pprint
import yaml

PROPERTIES = ["Items", "Player", "Rooms"]
PLAYERDATA = ["holding", "location", "current", "max"]
ITEMDATA = ["holds"]
DIRECTIONS = ["north", "south", "east", "west"]


def load(file_name="./dork/yaml/dork.yml"):
    """This will load a file into data.
    """
    try:
        with open(file_name) as file:
            data = yaml.safe_load(file.read())
    except IOError:
        return "Try again"
    return data


def save(data):
    """This will save player and room data to a file.
    Eventually this should also save maze data.
    """

    print("Attempting to save data.")

    file_name = "./dork/yaml/dorktest.yml"
    with open(file_name, 'w') as yaml_file:
        yaml_file.write(yaml.dump(data, default_flow_style=False))

    print("Save was successful.")


def pplayer(players, name, pdata):
    """Parses player data into useful info.
    """
    player = players[name]
    if pdata not in player:
        print(".")
    elif player[pdata] is None:
        print(f"There is no data in {name}.")
    else:
        other = player[pdata]
        print(f"Player data {name}: {other}.")


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
    data = load()
    print("Data that was loaded:")
    pprint(data)

    print("Checking rooms, items, and player data for errors...")
    for ppty in PROPERTIES:
        if ppty not in data:
            print(f"No {ppty} found.")
        if not isinstance(data[ppty], dict):
            print(f"{ppty} in data were not proper data.")
            return

    parseroom(data)
    parseitem(data)
    parseplayer(data)

    print("Attempting test save.")
    save(data)


def parseroom(data):
    """Parses room data.
    """
    rooms = data["Rooms"]
    for name in rooms:
        for direction in DIRECTIONS:
            path(rooms, name, direction)


def parseitem(data):
    """Parses item data.
    """
    items = data["Items"]
    for name in items:
        for idata in ITEMDATA:
            pitem(items, name, idata)


def parseplayer(data):
    """Parses player data.
    """
    players = data["Player"]
    for name in players:
        for pdata in PLAYERDATA:
            pplayer(players, name, pdata)


if __name__ == "__main__":  # pragma: no cover
    main()
