# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""

__all__ = ["Player", "Room", "GAME"]

GAME = None


class Game():
    """Creates and hold the game state
    """
    def __init__(self, data):
        self._data = data
        self.player = Player(data['player'])
        self.rooms = {room_name: Room(room) for room_name,
                      room in data.get('rooms').items()}
        self.items = {item_name: Item(item) for item_name,
                      item in data.get('items').items()}

    def save(self):
        """Will save the Game class
        """
        return {
            "player": self.player.save(),
            "rooms": {
                name: room.save()
                for name, room in self.rooms.items()
            }
        }


class Player():
    """ This is the player class
    """
    def __init__(self, data):
        self.location = data.get('location')
        self.next_location = data.get('next location')
        self.inventory = data.get('inventory')
        self.last_room = data.get('last room')

    def save(self):
        """Will save the player class
        """
        return {
            "location": self.location,
            "next location": self.next_location,
            "inventory": self.inventory,
            "last room": self.last_room,
        }


class Room():
    """A room on map
    """

    def __init__(self, data):
        self.messages = data.get('messages')
        self.door = data.get('door')
        self.paths = data.get('paths')

        # rooms['cell'].door['locked']
        # rooms['hallway'].messages['description']

    def save(self):
        """Will save the room class
        """
        return {
            'messages': self.messages,
            'door': self.door,
            'paths': self.paths,
        }


class Item():
    """Item in game
    """
    def __init__(self, data):
        self.description = data.get('description')

    def save(self):
        """Will save the room class
        """
        return {
            'description': self.description
            }
