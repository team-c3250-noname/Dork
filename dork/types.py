import dork.saveload as load

__all__ = ["Item", "Holder", "Player", "Room", "Path", "Map"]


class Map:
    """A map relating the rooms connectivity
        as well as the players/items within
    """
    def __init__(self):
        self.rooms = list()


class Game():
    """Creates and hold the game state
    """
    def __init__(self, data):
        self.player = Player(data['player'])
        self.room = [room for room in data.get('rooms')]


class Player():
    """ This is the player class
    """
    def __init__(self, data):
        self.location = data.get('location')
        self.next_location = data.get('next location')
        self.inventory = data.get('inventory')


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
