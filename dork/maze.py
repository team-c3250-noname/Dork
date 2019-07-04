"""Generates mazes
"""
from abc import ABC
from abc import abstractmethod
from collections import deque
from random import sample, choice, randint
from os import linesep

import networkx as nx
import pylab as plt

DIRECTIONS = {"up": 0, "down": 1, "left": 2, "right": 3}


class MazeGenerator(ABC):
    """Abstract maze generator
    """
    class Node:
        """helper class for node generation
        """
        ID = 0

        def __init__(self):
            self.id = self.__class__.ID
            self.__class__.ID += 1
            self.up, self.down, self.left, self.right = None, None, None, None

        def set_left_right(self, node, line_width):
            """sets this nodes left, or right depending if node
                 is left or right of this node in the line
            """
            if node.id % line_width == 0:
                if self.id-1 == node.id:
                    self.left = node.id
                    node.right = self
                return
            if node.id % line_width == 1:
                if self.id+1 == node.id:
                    self.right = node.id
                    node.left = self
                return
            if self.id+1 == node.id:
                self.right = node.id
                node.left = self
            if self.id-1 == node.id:
                self.left = node.id
                node.right = self

        def __hash__(self):
            return self.id

        def __str__(self):
            directions = [self.up, self.down, self.left, self.right]
            return str(self.id) + ":->" + "->".\
                join([str(hash(way)) if way else " " for way in directions])

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
    def _get_nx_nodes(self):
        """returns the nodes of the maze in nx acceptable type (integer)
        """
    @abstractmethod
    def get_nodes_and_edges(self):
        """returns the nodes and edges, insuring the last line closes the maze
        """
    @abstractmethod
    def _get_nx_edges(self):
        """returns the edge set of the maze for nx [(integer, integer),...]
        """


class Ellers(MazeGenerator):
    """Ellers maze
    """
    class Line:
        """Maze line consisting of nodes
        """
        def __init__(self, width):
            self.nodes = tuple([Ellers.Node() for _ in range(0, width)])
            self.sets = dict(zip([node for node in self.nodes],
                                 [set([node]) for node in self.nodes]))

        def __str__(self):
            groups = [str(group) for group in self.sets]
            return linesep.join(groups)

    def __init__(self, width=10):
        self.width = width
        self.lines = deque()
        self.end = None
        self.is_closed = False

    @staticmethod
    def _should_join():
        """returns random answer to should join?
        """
        return choice([0, 1])

    @staticmethod
    def _pairwise_random_wall(line):
        for i, j in zip(line.nodes, line.nodes[1:]):
            if Ellers._should_join():
                if line.sets[i] is line.sets[j]:
                    continue
                line.sets[i].add(j)
                line.sets[j] = line.sets[i]
                i.right = j
                j.left = i
            else:
                i.right = None
                j.left = None

    @staticmethod
    def _get_down_nodes(line):
        seen = {}
        down_indices = []
        for group in line.sets:
            if id(line.sets[group]) not in seen:
                population = line.sets[group]
                current_line_set = set(line.nodes)
                population = population.intersection(current_line_set)
                k = randint(1, len(population)-1) if len(population) > 1 else 1
                node_sample = sample(population, k)
                down_indices.append(node_sample)
                seen[id(line.sets[group])] = None
        return down_indices

    def generate(self):
        """generates a maze based on Ellers algorithm
        """
        line = Ellers.Line(self.width)
        while True:
            if self.is_closed:
                yield None
                continue
            Ellers._pairwise_random_wall(line)

            next_line = Ellers.Line(self.width)

            down_indices = Ellers._get_down_nodes(line)

            for down_nodes in down_indices:
                last_down_node = None
                for node in down_nodes:
                    next_node = next_line.nodes[hash(node) % self.width]
                    if last_down_node:
                        last_down_node.set_left_right(next_node, self.width)
                    previous_set = line.sets[node]
                    next_line.sets[next_node] = previous_set
                    next_line.sets[next_node].add(next_node)
                    next_node.up = node
                    node.down = next_node
                    last_down_node = next_node

            self.lines.append(line)
            self.end = next_line

            yield line
            line = next_line

    def open(self):
        self.is_closed = False

    def close(self):
        self.is_closed = True

    def _get_nx_edges(self):
        nodes = []
        for line in self.lines:
            nodes.extend(line.nodes)
        edges = []
        directions = tuple(DIRECTIONS.keys())
        for node in nodes:
            for direction in directions:
                if node.__dict__[direction]:
                    edges.append((hash(node), hash(node.__dict__[direction])))
        return edges

    def _get_nx_nodes(self):
        node_id = []
        for line in self.lines:
            node_id.extend([node.id for node in line.nodes])
        return node_id

    def get_nodes_and_edges(self):
        line = self.end
        for i, j in zip(line.nodes, line.nodes[1:]):
            if line.sets[i] is line.sets[j]:
                continue
            new_set = line.sets[j].union(line.sets[i])
            i.right = j
            j.left = i
            line.sets[j] = new_set
            line.sets[i] = new_set
        previous_line = self.lines[-1]
        for node in previous_line.nodes:
            if node.down:
                node.down.up = node
        self.lines.append(line)
        nodes = self._get_nx_nodes()
        edges = self._get_nx_edges()


        self.lines.clear()
        self.lines.append(previous_line)
        self.lines.append(line)

        return (nodes, edges)


class Maze:
    """Uses a maze generator to generate a maze
    """
    class Area:
        def __init__(self, node_id, name):
            self.node = node_id
            self.name = name
            self.in_nodes = {"up": None, "down": None, "left": None, "right": None}
            self.out_nodes = {"up": None, "down": None, "left": None, "right": None}
            self.paths = {"up": None, "down": None, "left": None, "right": None}

        def set_neighbor_nodes(self, neighbors, width):
            """sets the cells edges
            """
            x, y = self.node % width, int(self.node / width)
            for neighbor in neighbors:
                neighbor_x, neighbor_y = neighbor % width, int(neighbor / width)
                if neighbor_x < x:
                    self.out_nodes["left"] = neighbor
                    self.in_nodes["left"] = neighbor
                elif neighbor_x > x:
                    self.out_nodes["right"] = neighbor
                    self.in_nodes["right"] = neighbor
                elif neighbor_y < y:
                    self.out_nodes["up"] = neighbor
                    self.in_nodes["up"] = neighbor
                else:
                    self.out_nodes["down"] = neighbor
                    self.in_nodes["down"] = neighbor

    def __init__(self, maze_generator=Ellers, width=10, height=10):
        self.width = max(width, 10)
        self.height = 0
        if not issubclass(maze_generator, MazeGenerator):
            raise TypeError("Maze requires derived type of MazeGenerator")
        self.maze_generator = maze_generator(width)
        self.maze_line = self.maze_generator.generate()
        self.graph = nx.DiGraph()
        self.areas = {}
        self.views = []
        self.grow(max(height, 10))

    def get_graph(self):
        """returns a copy of the graph
        """
        return self.graph.copy()

    def claim_cell(self, name, x, y):
        """tags a cell as an owned area
        """
        if name in self.areas:
            raise KeyError(f"{name} area already used for cell {self.areas[name]}")
        node_id = x + y * self.width
        if node_id not in self.graph.nodes():
            raise IndexError(f"Cell at ({x}, {y}) as id {node_id} out of bounds")

        area = self.Area(node_id, name)
        area.set_neighbor_nodes(list(self.graph.neighbors(node_id)), self.width)
        self.areas[name] = area

    def _get_coordinates(self, node):
        return (node % self.width, int(node / self.width))

    def _get_node_way(self, node, way):
        x, y = self._get_coordinates(node)
        if way == "up":
            y -= 1
        elif way == "down":
            y += 1
        elif way == "left":
            x -= 1
        else:
            x += 1
        return x, y

    def _is_way_possible(self, node_id, way):
        x, y = self._get_node_way(node_id, way)
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True

    def get_path(self, area_name, direction):
        """ returns a list of nodes as a path
        """
        return self.areas[area_name][direction]

    def make_path(self, from_area, from_way, to_area, to_way):
        """connects two areas, breaks walls if needed
        """
        from_area = self.areas[from_area]
        to_area = self.areas[to_area]

        from_node = from_area.out_nodes[from_way]
        to_node = to_area.in_nodes[to_way]

        if from_node and to_node:
            if nx.has_path(self.graph, from_node, to_node):
                path = nx.shortest_path(self.graph, from_node, to_node)
                from_area.paths[from_way] = path
                to_area.paths[to_way] = path[::-1]
                return

        if not from_node:
            if not self._is_way_possible(from_area.node, from_way):
                print(f"Room {from_area.node} cannot go {from_way}")
                raise ValueError(f"Room {from_area.name} cannot go {from_way}")
            x, y = self._get_node_way(from_area.node, from_way)
            node_way = x + y * self.width
            self.graph.add_edge(from_area.node, node_way)
            self.graph.add_edge(node_way, from_area.node)
            from_node = node_way
        if not to_node:
            if not self._is_way_possible(to_area.node, to_way):
                raise ValueError(f"Room {to_area.name} cannot go {to_way}")
            x, y = self._get_node_way(to_area.node, to_way)
            node_way = x + y * self.width
            self.graph.add_edge(to_area.node, node_way)
            self.graph.add_edge(node_way, to_area.node)
            to_node = node_way
        if from_node and to_node:
            if nx.has_path(self.graph, from_node, to_node):
                path = nx.shortest_path(self.graph, from_node, to_node)
                from_area.paths[from_way] = path
                to_area.paths[to_way] = path[::-1]
        else:
            raise RuntimeError(f"path from {from_area.name} to {to_area.name} could not be made")

    def grow(self, line_count=10):
        """grows the maze
        """
        self.height += line_count
        line_count = max(line_count, 2)
        for i in range(0, line_count):
            next(self.maze_line)
            if not i % 2 and i > 2:
                nodes, edges = self.maze_generator.get_nodes_and_edges()
                self.graph.add_nodes_from(nodes)
                self.graph.add_edges_from(edges)
        nodes, edges = self.maze_generator.get_nodes_and_edges()
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)

if __name__ == "__main__": # pragma: no cover
    pass
