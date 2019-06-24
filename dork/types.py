# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""

__all__ = ["Item", "Holder", "Player", "Room", "Path", "Map"]


class Item:
    """A obtainable/holdable item
    """

    def __init__(self):
        self.holder = Holder()


class Holder:
    """A holder/container of items
    """

    def __init__(self):
        self.items = list()


class Room(Holder):
    """A room on the map

    Note: can only be entered through entraces
        or exited through exits.
    """

    def __init__(self):
        super(Room, self).__init__()
        self.map = Map()
        self.entrances = list()
        self.exits = list()
        self.players = list()


class Path:
    """A path between two rooms (i.e. a door or hallway)
    """

    def __init__(self):
        self.entrance = Room()
        self.exit = Room()


class Map:
    """A map relating the rooms connectivity
        as well as the players/items within
    """

    def __init__(self):
        self.rooms = list()


class Player():
    """ This is the player class
    """
    def __init__(self):
        self.location = 'cell'
        self.inventory = []


MY_PLAYER = Player()

ROOM_NAME = ''
DESCRIPTION = 'description'
LOCKED = False
ITEM = ''
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'

ZONE_MAP = {
    'cell': {
        ROOM_NAME: 'cell',
        DESCRIPTION: 'This is the starting location',
        LOCKED: False,
        ITEM: 'cellkey',
        UP: 'Hallway south',
        DOWN: '',
        LEFT: '',
        RIGHT: '',
    },
    'Hallway south': {
        ROOM_NAME: 'Hallway south',
        DESCRIPTION: 'Outside your cell',
        LOCKED: False,
        ITEM: '',
        UP: '',
        DOWN: 'cell',
        LEFT: '',
        RIGHT: '',
    },
}
