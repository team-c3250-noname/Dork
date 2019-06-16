from pprint import pprint
import yaml

ITEMS = ["Key to Armory", "Sword", "Torch", "Gold"]
DIRECTIONS = ["north", "south", "east", "west"]

def _load(file_name = "./dork/yaml/dork.yml"):
    with open(file_name) as file:
        data = yaml.safe_load(file.read())

    return data

def _save():
    # Decide how to format save data
    # For now we have a test dork.yml file
    return

def _path(rooms, name, direction):
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

def _item(rooms, name, item):
    room = rooms[name]
    if item not in room:
        print(f"{name} does not have {item} in it.")
    elif room[item] is None:
        print(f"There are no items in {name}.")
    elif room[item] not in rooms:
        print(f"{item} in {name} will lead to an error.")
    else:
        other = room[item]
        print(f"{other} is an item in {name}.")

def main():
    data = _load()
    print("Data that was loaded:")
    pprint(data)

    print("Checking room and item list...")
    if "Rooms" not in data:
        print("No rooms found.")
        return

    if "Items" not in data:
        print("No items found.")
        return

    if not isinstance(data["Rooms"], dict):
        print("Rooms in data were not proper data.")
        return

    if not isinstance(data["Items"], dict):
        print("Items in data were not proper data.")
        return

    rooms = data["Rooms"]
    for name in rooms:
        for direction in DIRECTIONS:
            _path(rooms, name, direction)

    items = data["Items"]
    for name in items:
        for item in ITEMS:
            _item(rooms, name, item)

if __name__ == "__main__":
    main()