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


class Player(Holder):
    """ This is the player class
    """
    def __init__(self):
        super(Player, self).__init__()
        self.location = 'cell'
        self.next_location = 'cell name'
        self.inventory = []
        self.room = Room()


MY_PLAYER = Player()

ROOM_NAME = ''
DESCRIPTION = 'description'
INSPECT = 'Inspection'
LOCKED = False
ITEM = ''
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'

ROOM_MAP = {
    'cell': {
        ROOM_NAME: 'cell',
        DESCRIPTION: """You find yourself in a jail cell with the door locked.
        As you look outside the bars, you can see a corridor extending in
        either direction. For now, you need to get out of here. Upon further
        inspection in the room, you note various shackles and torture
        instruments, a metal bed suspended from the wall with a chain, but
        nothing more""",
        INSPECT: """Upon checking under the bed, you find a key. How convenient
        for you, prisoner!""",
        LOCKED: False,
        ITEM: 'cell key',
        UP: 'Jail hallway',
        DOWN: '',
        LEFT: '',
        RIGHT: '',
    },
    'Jail hallway': {
        ROOM_NAME: 'Jail Hallway',
        DESCRIPTION: """A long, narrow hallway lined with cells and torches
        for light on either side. To your immediate left, there is a locked
        door. Upon further inspection of this door, you notice that the lock
        is rusted and falling apart. You attempt to pull it open with your
        bare hands, but it does not budge. Perhaps if you had something that
        would give you some leverage... To your right, down the corridor,
        there is a stairwell. The stairs lead up, but it is completely
        pitch black inside. You'll probably trip and hurt yourself without a
        source of light. You should be able to reach up and remove one of the
        torches from the wall.""",
        INSPECT: 'You inspect the room',
        LOCKED: False,
        ITEM: 'torch',
        UP: '',
        DOWN: 'cell',
        LEFT: 'Jail Armory',
        RIGHT: 'Stairwell',
    },
    'Stairwell': {
        ROOM_NAME: 'cell',
        DESCRIPTION: """Using the torch, you are able to see that the stairwell
        is decrepit and many steps have chunks missing, with others having
        pieces of rubble on them. You make your way carefully up the stairs and
        emerge at the top.""",
        INSPECT: 'You inspect the room',
        LOCKED: False,
        ITEM: '',
        UP: 'Jail Tower',
        DOWN: '',
        LEFT: 'Jail hallway',
        RIGHT: '',
    },
    'Jail Tower': {
        ROOM_NAME: 'Jail Tower',
        DESCRIPTION: """As you exit the stairwell and go outside, you find
        yourself atop a tower. It is raining hard and a storm is currently
        ongoing. You hear the sounds of thunder and see bright flashes of
        lightning every now and then. As you look over the edge of the tower,
        you see nothing but a raging ocean. """,
        INSPECT: """As you look around on top of the tower, you note that
        there is an iron bar leaned up against the wall, near the door you
        emerged from. You take the iron bar. It is cold in your hands and
        wet from the rain, but otherwise sturdy.""",
        LOCKED: False,
        ITEM: 'iron bar',
        UP: '',
        DOWN: 'Stairwell',
        LEFT: '',
        RIGHT: '',
    },
    'Jail Armory': {
        ROOM_NAME: 'Jail Armory',
        DESCRIPTION: """You enter the armory and note that the armor and weapon
        racks are all but empty. You also note the presence of a few target
        dummies and archery targets. """,
        INSPECT: """One of the dummies has a sword embedded in it. You are able
        to pull the sword from the dummy with a little effort.""",
        LOCKED: True,
        ITEM: 'sword',
        UP: '',
        DOWN: '',
        LEFT: '',
        RIGHT: 'Jail hallway',
    },
}
