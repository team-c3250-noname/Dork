# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""


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
