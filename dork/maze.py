"""Generates mazes
"""
from abc import ABC
from abc import abstractmethod
from collections import namedtuple
from random import sample, choice, randint
from itertools import product
from math import sqrt

import networkx as nx


class MazeGenerator(ABC):
    """Abstract maze generator
    """

    @abstractmethod
    def generate(self):
        """generates a maze with defined width,heights
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

    @staticmethod
    def _should_join():
        """returns random answer to should join?
        """
        chosen = choice([0, 1])
        return chosen

    def _get_set(self, node_id):
        return self.node_set_map[node_id]

    def _random_horizontal_edges(self, line):
        edges = []
        for i, j in zip(line, line[1:]):
            if Ellers._should_join():
                i_set = self._get_set(i)
                j_set = self._get_set(j)
                if i_set is not j_set:
                    i_set.add(j)
                    self.node_set_map[j] = i_set

                    j_set.remove(j)
                    if j_set.difference(set()) == set():
                        self.sets.remove(j_set)
                    edges.append((i, j))
                    edges.append((j, i))
        return edges

    def _random_vertical_nodes(self, line):
        seen = {}
        down_indices = []
        line_sets = {}

        kv_pairs = [(id(_set), _set) for _set in self.sets
                    for node_id in line if node_id in _set]
        line_sets.update(kv_pairs)

        for _set in line_sets.values():
            if id(_set) not in seen:
                population = _set
                current_line_set = set(line)
                population = population.intersection(current_line_set)
                k = randint(1, len(population)-1) if len(population) > 1 else 1
                node_sample = sample(population, k)
                down_indices.append(node_sample)
                seen[id(_set)] = None
        return down_indices

    def __init__(self, width=MIN):
        self.width = max(width, self.__class__.MIN)

        self.nodes = []
        self.edges = []

        self.sets = []
        self.node_set_map = {}

        self._end = []
        self.id_counter = 0

    def location(self, node_id):
        """ gets x,y coordinates for a n-width maze
        """
        return (node_id % self.width, int(node_id / self.width))

    def left(self, node_id):
        """ returns node left of node_id
        """
        x, y = self.location(node_id)
        x = x - 1
        return None if x < 0 else x + y * self.width

    def right(self, node_id):
        """ returns node right of node_id
        """
        x, y = self.location(node_id)
        x = x + 1
        return None if x >= self.width else x + y * self.width

    def up(self, node_id):
        """ returns node up of node_id
        """
        x, y = self.location(node_id)
        y = y - 1
        return None if y < 0 else x + y * self.width

    def down(self, node_id):
        """ returns node down of node_id
        """
        x, y = self.location(node_id)
        y = y + 1
        return None if y >= int(self.id_counter / self.width)\
            else x + y * self.width

    def _new_line(self):
        new_line = list(range(self.id_counter, self.id_counter + self.width))
        new_line_unique = [node_id for node_id in new_line
                           if node_id not in self.node_set_map]
        for node_id in new_line_unique:
            node_id_set = set([node_id])
            self.sets.append(node_id_set)
            self.node_set_map[node_id] = node_id_set

        self.id_counter += self.width
        return new_line

    def generate(self):
        """generates a maze with defined width,heights
        """
        current_line, next_line = self._new_line(), None
        self.nodes.extend(current_line)

        while True:
            if self._end is None:
                yield None
            horizontal_edges = self._random_horizontal_edges(current_line)
            vertical_nodes = self._random_vertical_nodes(current_line)

            next_line = self._new_line()
            vertical_edges = []

            for nodelist in vertical_nodes:
                for node in nodelist:
                    node_set = self.node_set_map[node]
                    down_node = self.down(node)
                    self.node_set_map[down_node].remove(down_node)
                    self.node_set_map[down_node] = node_set
                    node_set.add(down_node)
                    vertical_edges.append((node, down_node))
                    vertical_edges.append((down_node, node))

            edges = horizontal_edges
            edges.extend(vertical_edges)

            self.nodes.extend(next_line)
            self.edges.extend(edges)

            self._end = next_line
            yield (self.nodes, edges)
            current_line = next_line

    def close(self):
        """locks the maze, afterward the generator returns None
        """
        line = self._end
        for i, j in zip(line, line[1:]):
            i_set = self._get_set(i)
            j_set = self._get_set(j)
            if i_set is not j_set:
                self.edges.append((i, j))
                self.edges.append((j, i))
        self._end = None

    def get_nodes(self):
        """returns the nodes of the maze in nx acceptable type (integer)
        """
        if self._end is not None:
            raise RuntimeWarning(
                "Ellers maze generator should call close before use")
        return self.nodes

    def get_nodes_and_edges(self):
        """returns the nodes and edges, insuring the last line closes the maze
        """
        if self._end is not None:
            raise RuntimeWarning(
                "Ellers maze generator should call close before use")
        return (self.get_nodes(), self.get_edges())

    def get_edges(self):
        """returns the edge set of the maze for nx [(integer, integer),...]
        """
        if self._end is not None:
            raise RuntimeWarning(
                "Ellers maze generator should call close before use")
        return self.edges


class Maze:
    """Uses a maze generator to generate a maze
    """
    Node = namedtuple('Node', ['id', 'x', 'y'])
    Point = namedtuple('Point', ['x', 'y'])
    Box = namedtuple('Box', ['width', 'height'])

    class Area:
        """Maze area...
        """
        def __init__(self, *, x=0, y=0, width=1, height=1):
            self.origin = Maze.Point(x=x, y=y)
            self.box = Maze.Box(width=width, height=height)
            self.center = []
            self.up_border = []
            self.down_border = []
            self.left_border = []
            self.right_border = []

    MIN = 5

    def __init__(self, *, width=MIN, height=None,
                 filename=None, maze_generator=Ellers):
        self.width = max(Maze.MIN, width)
        self.filename = filename
        self.graph = nx.DiGraph()
        self.areas = {}
        self.is_closed = False
        assert issubclass(maze_generator, MazeGenerator),\
            f"Maze parameter maze_generator must be derived from MazeGenerator"
        if self.filename:
            raise NotImplementedError("file save load not done for maze")

        self._maze = maze_generator(self.width)
        self.generator = self._maze.generate()
        if height:
            for _ in range(0, height-1):
                next(self.generator)
            self.close()

    def size(self):
        """returns the number of nodes in the maze
        """
        if not self.is_closed:
            raise RuntimeWarning("Mazes are read only until closed")
        return len(self.graph.nodes())

    def grow(self, line_count=1):
        """grows the maze, returns (nodes<list>, edges<list of tuples>)
        """
        if self.graph.nodes():
            return (None, None)
        nodes, edges = [], []
        for _ in range(0, line_count):
            maze_nodes, maze_edges = next(self.generator)
            nodes.extend(maze_nodes)
            edges.extend(maze_edges)
        return nodes, edges

    def close(self):
        """calls the maze generator close to finalize EoM line
        """
        self.is_closed = True
        self._maze.close()
        self.graph.add_nodes_from(self._maze.get_nodes())
        self.graph.add_edges_from(self._maze.get_edges())

    def _get_area_offset(self, area, dx, dy):
        return area.origin.x+dx + (area.origin.y+dy) * self.width

    def _grid_connect(self, area):
        offsets = product(range(0, area.box.width), range(0, area.box.height))
        edges = []
        center_nodes = []

        for dx, dy in offsets:
            if not any([dx == 0,
                        dy == 0,
                        dy == area.box.height-1,
                        dx == area.box.width-1]):
                center_nodes.append(self._get_area_offset(area, dx, dy))
            else:
                if dy == 0:
                    area.up_border.append(self._get_area_offset(area, dx, dy))
                if dy == area.box.height-1:
                    area.down_border.append(self._get_area_offset(area,
                                                                  dx, dy))
                if dx == 0:
                    area.left_border.append(self._get_area_offset(area,
                                                                  dx, dy))
                if dx == area.box.width-1:
                    area.right_border.append(self._get_area_offset(area,
                                                                   dx,
                                                                   dy))

        area.center = center_nodes
        for node in center_nodes:
            edges.extend([(node, self._maze.down(node)),
                          (self._maze.down(node), node)])
            edges.extend([(node, self._maze.up(node)),
                          (self._maze.up(node), node)])
            edges.extend([(node, self._maze.left(node)),
                          (self._maze.left(node), node)])
            edges.extend([(node, self._maze.right(node)),
                          (self._maze.right(node), node)])

        borders = [area.up_border, area.down_border,
                   area.left_border, area.right_border]
        for edge in borders:
            one_way = list(zip(edge, edge[1:]))
            edges.extend(one_way)
            other_way = [(v, u) for (u, v) in one_way]
            edges.extend(other_way)

        self.graph.add_edges_from(edges)

    def _get_direction(self, nids, node):
        possible = [self._maze.up(node),
                    self._maze.down(node),
                    self._maze.left(node),
                    self._maze.right(node)]
        return list(filter(lambda x: x not in nids and x, possible))[0]

    def _stitch_components(self, components):
        borders = {id(component): Maze.Area() for component in components}
        nodes = []

        for component in components:
            for node in component:
                x, y = node % self.width, int(node / self.width)
                nodes.append(Maze.Node(id=node, x=x, y=y))

            x_range = (min(nodes, key=lambda node: node.x),
                       max(nodes, key=lambda node: node.x))
            y_range = (min(nodes, key=lambda node: node.y),
                       max(nodes, key=lambda node: node.y))
            x_range = range(x_range[0].x, x_range[1].x)
            y_range = range(y_range[0].y, y_range[1].y)

            lines = []
            for line in y_range:
                lines.append([])
                for node in nodes:
                    if node.y == line:
                        lines[-1].append(node)

            def nodex(node):
                return node.x

            def nodey(node):
                return node.y
            for line in lines:
                borders[id(component)].right_border.append(max(line,
                                                               key=nodex).id)
                borders[id(component)].left_border.append(min(line,
                                                              key=nodex).id)

            lines = []
            for line in x_range:
                lines.append([])
                for node in nodes:
                    if node.x == line:
                        lines[-1].append(node)

            for line in lines:
                borders[id(component)].up_border.append(max(line,
                                                            key=nodey).id)
                borders[id(component)].down_border.append(min(line,
                                                              key=nodey).id)

            self._component_wise_combine(borders)

    def _component_wise_combine(self, walls):
        for component_one, component_two in product(walls.values(),
                                                    walls.values()):
            if component_one is not component_two:
                directions = ["up", "down", "left", "right"]
                inverse = {"up": "down", "down": "up",
                           "left": "right", "right": "left"}
                possible_edges = []
                for direction in directions:
                    candidates = map(getattr(self._maze, direction),
                                     getattr(component_one, direction +
                                             "_border")
                                     )
                    compare_to = []
                    compare_to.extend(component_two.up_border)
                    compare_to.extend(component_two.down_border)
                    compare_to.extend(component_two.left_border)
                    compare_to.extend(component_two.right_border)
                    possible_edges.extend([(candidate,
                                            getattr(self._maze,
                                                    inverse[direction])
                                            (candidate))
                                           for candidate in candidates if
                                           candidate in compare_to])
                if possible_edges:
                    self.graph.add_edges_from(possible_edges)
                    self.graph.add_edges_from([(v, u)
                                               for u, v in possible_edges])

    def _get_area_edges(self, nodes):
        """returns all edges for an areas nodes
        """
        area_edges = [list(self.graph.in_edges(node.id, data=False))
                      for node in nodes]
        in_edges_all = [edge for edges in area_edges for edge in edges]

        area_edges = [list(self.graph.out_edges(node.id, data=False))
                      for node in nodes]
        area_edges = [edge for edges in area_edges for edge in edges]
        area_edges.extend(in_edges_all)
        return area_edges

    def _get_area_nodes(self, area):
        """gets areas nodes
        """
        offsets = product(range(0, area.box.width), range(0, area.box.height))
        nodes = []
        for dx, dy in offsets:
            node = Maze.Node(id=self._get_area_offset(area, dx, dy),
                             x=area.origin.x+dx, y=area.origin.y+dy)
            if node.id not in self.graph:
                raise IndexError(f"maze graph does not have node {node.id}")
            nodes.append(node)
        return nodes

    def _get_components(self):
        """get components excluding areas
        """
        components = []
        for component in nx.strongly_connected_components(self.graph):
            if any([self._get_area_offset(area, 0, 0) in component
                    for area in self.areas.values()]):
                continue
            components.append(component)
        return components

    def distance(self, node_id_pair):
        """calculates distance between node ids
        """
        node_id1, node_id2 = node_id_pair[0], node_id_pair[1]
        x_1, y_1 = node_id1 % self.width, int(node_id1 / self.width)
        x_2, y_2 = node_id2 % self.width, int(node_id2 / self.width)
        return (node_id_pair, sqrt(pow((x_2-x_1), 2)+pow((y_2-y_1), 2)))

    def claim_area(self, name, area):
        """claims a set of nodes, makes maze consistent
        """
        if not self.is_closed:
            raise RuntimeWarning("Mazes are read only until closed")

        if name in self.areas:
            raise KeyError(f"area {name} already used")

        if any([area.origin.x < 0, area.origin.y < 0,
                area.box.width < 0, area.box.height < 0]):
            raise ValueError("origin point and\
                            dimensions must be positive")

        if area.box.width > self.width or\
           area.box.height > int(len(self.graph.nodes()) / self.width):
            raise ValueError(f"area width or height too large")

        if area.origin.x > self.width or\
           area.origin.y > int(len(self.graph.nodes()) / self.width):
            raise ValueError(f"origin point outside maze bounds")

        nodes = self._get_area_nodes(area)

        nids = [node.id for node in nodes]

        area_edges = self._get_area_edges(nodes)

        self.graph.remove_edges_from(area_edges)

        ext_nodes = [edge[0] for edge in area_edges if edge[0] not in nids]
        ext_nodes.extend([edge[1] for edge in area_edges
                          if edge[1] not in nids])
        ext_nodes = set(ext_nodes)

        self._grid_connect(area)

        for external_node in ext_nodes:
            if len(nx.descendants(self.graph, external_node)) <\
               len(self.graph.nodes()) - len(nids):
                node = self._get_direction(nids, external_node)
                self.graph.add_edge(node, external_node)
                self.graph.add_edge(external_node, node)

        self.areas[name] = area

        components = self._get_components()

        if len(components) > 1:
            self._stitch_components(components)

        components = self._get_components()

        if len(components) > 1:  # an attempt was made, now SMASH...
            for component_one, component_two in zip(components,
                                                    components[1:]):
                component_product = product(component_one, component_two)
                edge = min(map(self.distance, component_product),
                           key=lambda edge: edge[-1])
                self.graph.add_edge(edge[0], edge[1])
                self.graph.add_edge(edge[1], edge[0])

    def get_path(self, from_area_name, from_way, to_area_name, to_way):
        """generates path for two areas if possible, returns none or path<list>
        """
        if not self.is_closed:
            raise RuntimeWarning("Mazes are read only until closed")
        from_area = self.areas[from_area_name]
        to_area = self.areas[to_area_name]

        from_node = choice(getattr(from_area, from_way + "_border"))
        to_node = choice(getattr(to_area, to_way + "_border"))

        from_next = getattr(self._maze, from_way)(from_node)
        to_next = getattr(self._maze, to_way)(to_node)

        if not from_next or not to_next:
            return []

        path = nx.shortest_path(self.graph, source=from_next, target=to_next)
        path.append((to_area_name, to_node))
        path.insert(0, (from_area_name, from_node))

        return path
