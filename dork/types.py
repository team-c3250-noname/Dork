import dork.saveload as load

__all__ = ["Item", "Holder", "Player", "Room", "Path", "Map", "GAME"]

GAME = None


class Game():
    """Creates and hold the game state
    """
    def __init__(self, data):
        self._data = data
        self.player = Player(data['player'])
        self.rooms = {room_name: Room(room) for room_name, room in data.get('rooms').items()}
    
    def save(self):
        return {
            "player": self.player.save(),
            "rooms": {
                name: room.save()
                for name, room in self.room.items()
            }
        }
    


class Player():
    """ This is the player class
    """
    def __init__(self, data):
        self.location = data.get('location')
        self.next_location = data.get('next location')
        self.inventory = data.get('inventory')
    
    def save(self):
        return {
            "location": self.location,
            "next location": self.next_location,
            "inventory": self.inventory,
        }


class Room():
    """A room on the map
    Note: can only be entered through entraces
        or exited through exits.
    """

    def __init__(self, data):
        self.messages = data.get('messages')
        self.door = data.get('door')
        self.paths = data.get('paths')

        # rooms['cell'].door['locked']
        # rooms['hallway'].messages['description']

    def save(self):
        return {
            'locked': self.locked,
            'unlock': self.unlock,
        }
