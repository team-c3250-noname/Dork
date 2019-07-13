"""Generates mazes
"""
from abc import ABC
from abc import abstractmethod
from collections import namedtuple
from random import sample, choice, randint

import networkx as nx

DIRECTIONS = {"up": 0, "down": 1, "left": 2, "right": 3}


class MazeGenerator(ABC):
    """Abstract maze generator
    """
    Node = namedtuple('Node', ['id', 'x', 'y'])

    @abstractmethod
    def generate(self):
        """generates a maze with defined width,heights
        """
    @abstractmethod
    def open(self):
        """opens a closed maze, at the bottom of the maze
        """
    @abstractmethod
    def close(self):
        """locks the maze, afterward the generator returns None
        """
    @abstractmethod
    def get_nodes(self):
        """returns the nodes of the maze in nx acceptable type (integer)
        """
    @abstractmethod
    def get_nodes_and_edges(self):
        """returns the nodes and edges, insuring the last line closes the maze
        """
    @abstractmethod
    def get_edges(self):
        """returns the edge set of the maze for nx [(integer, integer),...]
        """

class Ellers(MazeGenerator):
    """Ellers maze, grows down.
    """
    MIN = 2
    
    def __init__(self, width=MIN):
        self.width = max(width, self.__class__.MIN)
        self.nodes = []
        self.edges = dict()
        self.id_counter = 0

    def location(self, node_id):
        return (node_id % self.width, int(node_id / self.width))

    def left(self, node_id):
        x, y = self.location(node_id)
        x = x - 1
        return None if x < 0 else x + y * self.width
    
    def right(self, node_id):
        x, y = self.location(node_id)
        x = x + 1
        return None if x >= self.width else x + y * self.width

    def up(self, node_id):
        x, y = self.location(node_id)
        y = y - 1
        return None if y < 0 else x + y * self.width
    
    def down(self, node_id):
        x, y = self.location(node_id)
        y = y + 1
        return None if y > int(self.nodes[-1] / self.width)\
                    else x + y * self.width
    
    def _new_line(self):
        new_line = list(range(self.id_counter, self.width))
        self.id_counter += self.width
        return new_line

    def generate(self):
        """generates a maze with defined width,heights
        """
        current_line, next_line = self._new_line(), None
        while True:
            current_line = self._new_line()

            self.nodes.extend(current_line)

            next_line = self._new_line()
            yield current_line
            current_line = next_line
            

            
        

    def open(self):
        """opens a closed maze, at the bottom of the maze
        """
        pass

    def close(self):
        """locks the maze, afterward the generator returns None
        """
        pass

    def get_nodes(self):
        """returns the nodes of the maze in nx acceptable type (integer)
        """
        pass

    def get_nodes_and_edges(self):
        """returns the nodes and edges, insuring the last line closes the maze
        """
        pass

    def get_edges(self):
        """returns the edge set of the maze for nx [(integer, integer),...]
        """
        pass


class Maze:
    """Uses a maze generator to generate a maze
    """
    pass

if __name__ == "__main__":
    maze = Ellers()
    maze_gen = maze.generate()
    next(maze_gen)
    next(maze_gen)
