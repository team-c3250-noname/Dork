# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""
import networkx as nx
import warnings
warnings.filterwarnings("ignore")
import pylab as plt
__all__ = ["Player", "Room", "GAME"]

GAME = None

class Map():
    """Map class updates with player location change...
    """
    class Point:
        def __init__(self, *, x=0, y=0):
            self.x = x
            self.y = y

    @staticmethod
    def _construct_minimap(minimap, nodes, rooms):
        origins = {}
        for name, room in rooms.items():
            for direction in ["up", "right", "left", "down"]:
                if room.paths[direction]:
                    if name not in origins:
                        origins[name] = Map.Point(x=0, y=0)
                    if room.paths[direction] not in origins:
                        origins[room.paths[direction]] = Map.Point(x=0, y=0)
                    x, y = (origins[name].x, origins[name].y)
                    if direction == "up":
                        y -= 1
                    if direction == "down":
                        y += 1
                    if direction == "left":
                        x -= 1
                    if direction == "right":
                        x += 1
                    origins[room.paths[direction]] = Map.Point(x=x, y=y)
                    minimap.add_edge(nodes[name],
                                     nodes[room.paths[direction]])
        return origins, minimap

    @staticmethod
    def _setup_window(corner_offset=0.05, width_of_screen=0.3):
        fig_manager = plt.get_current_fig_manager()
        fig_manager.set_window_title("Team NoName - Dork - Map")
        width = int(fig_manager.window.winfo_screenwidth()*width_of_screen)
        height = width
        x, y = fig_manager.window.winfo_screenwidth()-width-int(height*corner_offset),\
               fig_manager.window.winfo_screenheight()-height-int(height*corner_offset)
        fig_manager.window.wm_deiconify()
        fig_manager.window.wm_geometry(f"{width}x{height}+{x}+{y}")
        fig_manager.window.children["!navigationtoolbar2tk"].pack_forget()
        fig_manager.window.overrideredirect(True)
        plt.ion()

    def __init__(self, game):
        self._game = game
        rooms = game.rooms
        minimap = nx.Graph()
        nodes = {name: node_id for name, node_id in
                 zip(rooms.keys(), range(0, len(rooms.keys())))}
        minimap.add_nodes_from(nodes.values())
        origins, minimap = Map._construct_minimap(minimap, nodes, rooms)

        dx = min(origins.values(), key=lambda origin: origin.x).x
        dy = min(origins.values(), key=lambda origin: origin.y).y

        if dx < 0:
            for origin in origins.values():
                origin.x += abs(dx)
        if dy < 0:
            for origin in origins.values():
                origin.y += abs(dy)

        width = max(origins.values(), key=lambda origin: origin.x).x + 1
        self.origins = origins
        self.map = {room:{"node_id": None, "edges": []} for room in origins}
        for name, origin in origins.items():
            node_id = origin.x + origin.y * width
            nodes[nodes[name]] = node_id
            self.map[name]["node_id"] = node_id
        for name, origin in origins.items():
            for edge in minimap.edges(nodes[name]):
                self.map[name]["edges"].append(nodes[edge[1]])
        
        Map._setup_window()
        self.show()

    def show(self):
        """Displays the graph as a networkkx plot
        """
        plt.clf()
        labels = {node_info["node_id"]:room for room,
                  node_info in self.map.items()}
        max_y = max(self.origins.values(), key=lambda node: node.y).y
        positions = {self.map[room]["node_id"]:(origin.x, abs(origin.y-max_y))
                     for room, origin in self.origins.items()}
        color_map = ["blue"  for _ in labels]
        color_map[list(labels.values())\
                  .index(self._game.player.position["location"])] = "red"
        minimap = nx.Graph()
        minimap.add_nodes_from([node_info["node_id"]
                                for room, node_info in self.map.items()])
        minimap.add_edges_from([(node_info["node_id"], e_node)
                                for room, node_info in self.map.items()
                                for e_node in node_info["edges"]])
        nx.draw(minimap, pos=positions, node_color=color_map, node_size=100)
        delta = 0.1
        pos_higher = {k:(v[0], v[1]+delta) for k,v in positions.items()}
        nx.draw_networkx_labels(minimap, pos_higher, labels)
        plt.margins(0.2)
        plt.show()

    def update(self):
        """update the figure on game-state change
        """
        self.show()

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
        self.map = Map(self)

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
