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

    def __init__(self, data):
        super(Room).__init__()
        self.room_name = data.get('room_name')
        self.description = data.get('description')
        self.inspect = data.get('inspect')
        self.item = data.get('item')
        self.connections = [Connect(connection) for connection in data.get('connections', [])]


class Connect():
    """subclass to room to include the way to check the locked state of rooms
    """

    def __init__(self, data):
        self.locked = data.get('locked')
        self.unlock = data.get('unlock')
        self.connection = data.get('connection')
