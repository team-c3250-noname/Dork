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


class Map:
    """A map relating the rooms connectivity
        as well as the players/items within
    """

    def __init__(self):
        self.rooms = list()


class Player(Holder):
    """ This is the player class
    """
    def __init__(self, location, next_location):
        super(Player, self).__init__()
        self.location = location
        self.next_location = next_location
        self.inventory = []


class Room():
    """A room on the map
    Note: can only be entered through entraces
        or exited through exits.
    """

    def __init__(self, room_name, description, inspect, item, locked, unlock, connections):
        super(Room).__init__()
        self.room_name = room_name
        self.description = description
        self.inspect = inspect
        self.item = item
        self.locked = locked
        self.unlock = unlock
        self.connections = connections


class Connect(Room):
    """subclass to room to include the way to check the locked state of rooms
    """

    def __init__(self, locked, unlock, connection):
        super(Connect).__init__()
        self.locked = locked
        self.unlock = unlock
        self.connection = connection

CELL = Room('cell', 'This is a jail cell', 'You find a key', 'cell key')
JAIL_HALLWAY = Room('jail hallway', 'This is a jail cell', 'You find a torch', 'torch')
STAIRWELL = Room('stairwell', 'This is the stairwell', '', '')
JAIL_TOWER = Room('jail tower', 'This is the jail tower', 'You find a iron bar', 'iron bar')
JAIL_ARMORY = Room('jail armory', 'This is the jail armory', 'You find a sword', 'sword')
BOSS_ROOM = Room('boss room', 'This is the boss room', '', '')
VAULT = Room('vault', 'This is the vault', 'You find gold', 'gold')
ENTRANCE = Room('entrance', 'This is entrance', '', '')

CELL_CONNECTION = Connect(False, '', {'north': JAIL_HALLWAY})
JAIL_HALLWAY_CONNECTION = Connect(True, '', {'south': CELL, 'west': JAIL_ARMORY, 'east': STAIRWELL})
STAIRWELL_CONNECTION = Connect(True, '', {'north': JAIL_TOWER, 'west': JAIL_HALLWAY})
JAIL_TOWER_CONNECTION = Connect(False, '', {'south': STAIRWELL})
JAIL_ARMORY_CONNECTION = Connect(True, '', {'north': BOSS_ROOM, 'east': JAIL_HALLWAY})
BOSS_ROOM_CONNECTION = Connect(True, '', {'north': ENTRANCE, 'south': JAIL_ARMORY, 'west': VAULT})
VAULT_CONNECTION = Connect(False, '', {'east': BOSS_ROOM})
ENTRANCE_CONNECTION = Connect(False, '', {'south': BOSS_ROOM})


MY_PLAYER = Player(CELL, '', [''])

ROOM_NAME = ''
DESCRIPTION = 'description'
INSPECT = 'Inspection'
LOCKED = False
UNLOCK = 'unlock item'
ITEM = 'room item'
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'

ROOM_MAP = {
    'cell': {
        ROOM_NAME: 'cell',
        DESCRIPTION: """
        You find yourself in a jail cell with the door locked.
        As you look outside the bars, you can see a corridor extending in
        either direction. For now, you need to get out of here. Upon further
        inspection in the room, you note various shackles and torture
        instruments, a metal bed suspended from the wall with a chain, but
        nothing more.""",
        INSPECT: """Upon checking under the bed, you find a key. How convenient
        for you, prisoner!""",
        LOCKED: False,
        UNLOCK: '',
        ITEM: 'cell key',
        UP: 'Jail hallway',
        DOWN: '',
        LEFT: '',
        RIGHT: '',
    },
    'Jail hallway': {
        ROOM_NAME: 'Jail Hallway',
        DESCRIPTION: """
        A long, narrow hallway lined with cells and torches for light on
        either side. To your immediate left, there is a crumbling wall.
        Perhaps if you had something that could help destroy it...
        To your right, down the corridor, there is a stairwell. The stairs
        lead up, but it is completely pitch black inside. You'll probably
        trip and hurt yourself without a source of light. You should be
        able to reach up and remove one of the torches from the wall.""",
        INSPECT: 'You inspect the room',
        LOCKED: True,
        UNLOCK: 'cell key',
        ITEM: 'torch',
        UP: '',
        DOWN: 'cell',
        LEFT: 'Jail Armory',
        RIGHT: 'Stairwell',
    },
    'Stairwell': {
        ROOM_NAME: 'Stairwell',
        DESCRIPTION: """
        Using the torch, you are able to see that the stairwell
        is decrepit and many steps have chunks missing, with others having
        pieces of rubble on them. You make your way carefully up the stairs and
        emerge at the top.""",
        INSPECT: 'You inspect the room',
        LOCKED: True,
        UNLOCK: 'torch',
        ITEM: '',
        UP: 'Jail Tower',
        DOWN: '',
        LEFT: 'Jail hallway',
        RIGHT: '',
    },
    'Jail Tower': {
        ROOM_NAME: 'Jail Tower',
        DESCRIPTION: """
        As you exit the stairwell and go outside, you find yourself atop a
        tower. It is raining hard and a storm is currently ongoing. You
        hear the sounds of thunder and see bright flashes of lightning
        every now and then. As you look over the edge of the tower,
        you see nothing but a raging ocean. """,
        INSPECT: """
        As you look around on top of the tower, you note that
        there is an iron bar leaned up against the wall, near the door you
        emerged from. You take the iron bar. It is cold in your hands and
        wet from the rain, but otherwise sturdy.""",
        LOCKED: False,
        UNLOCK: '',
        ITEM: 'iron bar',
        UP: '',
        DOWN: 'Stairwell',
        LEFT: '',
        RIGHT: '',
    },
    'Jail Armory': {
        ROOM_NAME: 'Jail Armory',
        DESCRIPTION: """
        You enter the armory and note that the armor and weapon
        racks are all but empty. You also note the presence of a few target
        dummies and archery targets. """,
        INSPECT: """
        One of the dummies has a sword embedded in it. You are able
        to pull the sword from the dummy with a little effort.""",
        LOCKED: True,
        UNLOCK: 'iron bar',
        ITEM: 'sword',
        UP: '',
        DOWN: '',
        LEFT: '',
        RIGHT: 'Jail hallway',
    },
    'Boss room': {
        ROOM_NAME: 'Boss room',
        DESCRIPTION: """
        You have entered the boss room
        """,
        INSPECT: """
        """,
        LOCKED: True,
        UNLOCK: 'sword',
        ITEM: '',
        UP: '',
        DOWN: 'Jail Armory',
        LEFT: 'Vault',
        RIGHT: '',
    },
    'Vault': {
        ROOM_NAME: 'Vault',
        DESCRIPTION: """
        This is the treasury
        """,
        INSPECT: """
        """,
        LOCKED: False,
        UNLOCK: '',
        ITEM: '',
        UP: '',
        DOWN: '',
        LEFT: '',
        RIGHT: 'Boss Room',
    },
    'Entrance': {
        ROOM_NAME: 'Entrance',
        DESCRIPTION: """
        This is the entrance to the jail
        """,
        INSPECT: """
        """,
        LOCKED: False,
        UNLOCK: '',
        ITEM: '',
        UP: '',
        DOWN: 'Boss Room',
        LEFT: '',
        RIGHT: '',
    },
}
