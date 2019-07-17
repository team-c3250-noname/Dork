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
        self.npc = {npc_name: Nonplayer(npc) for npc_name,
                    npc in data.get('npc').items()}

    def save(self):
        """Will save the Game class
        """
        return {
            "player": self.player.save(),
            "rooms": {
                name: room.save()
                for name, room in self.rooms.items()},
            "items": {
                name: item.save()
                for name, item in self.items.items()},
            "npc": {
                name: npc.save()
                for name, npc in self.npc.items()},
        }


class Player():
    """ This is the player class
    """
    def __init__(self, data):
        self.position = data.get('position')
        self.inventory = data.get('inventory')
        self.stats = data.get('stats')

    def save(self):
        """Will save the player class
        """
        return {
            "position": self.position,
            "inventory": self.inventory,
            "stats": self.stats,
        }


class Room():
    """A room on map
    """

    def __init__(self, data):
        self.messages = data.get('messages')
        self.door = data.get('door')
        self.fight = data.get('fight')
        self.paths = data.get('paths')

    def save(self):
        """Will save the room class
        """
        return {
            'messages': self.messages,
            'door': self.door,
            'fight': self.fight,
            'paths': self.paths,
        }


class Item():
    """Item in game
    """
    def __init__(self, data):
        self.description = data.get('description')
        self.damage = data.get('damage')

    def save(self):
        """Will save the room class
        """
        return {
            'description': self.description,
            'damage': self.damage,
            }


class Nonplayer():
    """Creates the NPC class
    """
    def __init__(self, data):
        self.health = data.get('health')
        self.attack = data.get('attack')

    def save(self):
        """Will save the room class
        """
        return {
            'health': self.health,
            'attack': self.attack,
            }
