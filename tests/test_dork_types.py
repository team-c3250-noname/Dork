"""tests types not covered in other test files
"""
import yaml
from dork.types import Map, Game, Room


def dork_test_map():
    """tests map class
    """
    with open('./dork/yaml/default.yml') as file:
        data = yaml.safe_load(file.read())

    room = {room_name: Room(room) for room_name,
            room in data.get('rooms').items()}

    game = Game(data)
    minimap = Map(game)
    assert all([room_name in minimap.origins for room_name in room]),\
        "atleast one room was not assigned an origin"
    assert all([room_name in minimap.map for room_name in room]),\
        "atleast one room name was not found in the map"
    assert all([node_info["edges"] for _, node_info in minimap.map.items()]),\
        "room map is not fully connected"

    minimap.update()
