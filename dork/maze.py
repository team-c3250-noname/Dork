"""Generates mazes
"""
from abc import ABC
from abc import abstractmethod
from random import sample, choice, randint
from itertools import product
from math import sqrt

import networkx as nx


class MazeGenerator(ABC):
    """Abstract maze generator
    """

    @abstractmethod
    def generate(self):
        """generates a maze with defined width, line by line


        Yields:
            A 2-tuple list of node identifiers and edge tuples
            or empty 2-tuple list if closed has been called

            ([0,1,2,3...], [(0,1), (3,2), ...])
        """

    @abstractmethod
    def close(self):
        """locks the maze
        """
    @abstractmethod
    def get_nodes(self):
        """returns the node list of the maze
        """
    @abstractmethod
    def get_nodes_and_edges(self):
        """returns the nodes and edges, insuring the last line closes the maze
        """
    @abstractmethod
    def get_edges(self):
        """returns the edge list of the maze as 2-tuple list
        """


class Ellers(MazeGenerator):
    """Ellers builds a maze based on fixed-width line generation using sets

    Coordinates with (0,0) at the top left corner and (width,height) at
    bottom right corner.

    Initialize the maze with a fixed width, then call the generate member
    to get a generator. Pass it to next to add lines to the maze. When done
    call close to append the last line, use the nodes and edges in networkx.

    Attributes:
        nodes: list of integers as node identifiers
        edges: list of edge tuples (node id, node id)
        sets: list of sets that build the maze
        node_set_map: dictionary maps node identifiers to sets
        id_counter: incrementing integer for unique identifiers

    See Also:
        weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm
    """
    MIN = 2

    @staticmethod
    def _should_join():
        chosen = choice([0, 1])
        return chosen

    def _get_set(self, node_id):
        return self.node_set_map[node_id]

    def _random_horizontal_edges(self, line):
        """Returns pair-wise edge list for this line

        Iterates over each pair of nodes in the line, randomly
        connecting them by creating an edge and assigning their
        them to the same set.

        Args:
            line: list of integers as node identifiers

        Returns:
            edges: list of 2-tuple intergers as node identifers [(0, 1)...]
        """
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
        """Returns list of integers as node identifiers

        Selects [1,n) nodes from the line to connect to the next line

        Args:
            line: list of integers as node identifiers

        Returns:
            edges: list of 2-tuple intergers as node identifers [(0, 1)...]
        """
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
        self._width = max(width, self.__class__.MIN)

        self.nodes = []
        self.edges = []

        self.sets = []
        self.node_set_map = {}

        self._end = []
        self.id_counter = 0

    def location(self, node_id):
        """ gets x,y coordinates for a n-width maze

        Args:
            node_id: integer

        Returns:
            coordinates as 2-integer-tuple
        """
        return (node_id % self._width, int(node_id / self._width))

    def left(self, node_id):
        """ returns node left of node_id

        Args:
            node_id: integer

        Returns:
            positive integer

        Raises:
            IndexError: coordinates must decompose into positive x,y components
        """
        x, y = self.location(node_id)
        x = x - 1
        if x < 0:
            raise IndexError("node_id cannot have negative x coordinate")
        return x + y * self._width

    def right(self, node_id):
        """ returns node left of node_id

        Args:
            node_id: integer

        Returns:
            positive integer

        Raises:
            IndexError: coordinates must decompose into positive x,y components
        """
        x, y = self.location(node_id)
        x = x + 1
        if x >= self._width:
            raise IndexError("node_id cannot have x coordinate\
                             larger than or equal to width")
        return x + y * self._width

    def up(self, node_id):
        """ returns node left of node_id

        Args:
            node_id: integer

        Returns:
            positive integer

        Raises:
            IndexError: coordinates must decompose into positive x,y components
        """
        x, y = self.location(node_id)
        y = y - 1
        if y < 0:
            raise IndexError("node_id cannot have negative y coordinate")
        return x + y * self._width

    def down(self, node_id):
        """ returns node left of node_id

        Args:
            node_id: integer

        Returns:
            positive integer

        Raises:
            IndexError: coordinates must decompose into positive x,y components
        """
        x, y = self.location(node_id)
        y = y + 1
        if y >= int(self.id_counter / self._width):
            raise IndexError("node_id cannot have y coordinate\
                             larger than or equal to maze height")
        return x + y * self._width

    def _new_line(self):
        new_line = list(range(self.id_counter, self.id_counter + self._width))
        new_line_unique = [node_id for node_id in new_line
                           if node_id not in self.node_set_map]
        for node_id in new_line_unique:
            node_id_set = set([node_id])
            self.sets.append(node_id_set)
            self.node_set_map[node_id] = node_id_set

        self.id_counter += self._width
        return new_line

    def generate(self):
        """Yields a new line

        When calling this function store result in a variable and pass it to
        next() to get the next line as a node-list, edge-list tuple

        """
        current_line, next_line = self._new_line(), None
        self.nodes.extend(current_line)

        while True:
            if self._end is None:
                yield ([], [])
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
        """see base class
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
        """see base class
        """
        if self._end is not None:
            raise RuntimeWarning(
                "Ellers maze generator should call close before use")
        return self.nodes

    def get_nodes_and_edges(self):
        """see base class
        """
        if self._end is not None:
            raise RuntimeWarning(
                "Ellers maze generator should call close before use")
        return (self.get_nodes(), self.get_edges())

    def get_edges(self):
        """see base class
        """
        if self._end is not None:
            raise RuntimeWarning(
                "Ellers maze generator should call close before use")
        return self.edges


class Maze:
    """Uses a maze generator to generate a maze

    Attributes:
        width: integer number of cells per line in the maze
        height: integer number of lines
        graph: Networkx directional graph
        areas: dictionary using room name as key to Maze.Area instances
        is_closed: boolean, True if the maze has a capped end line
        generator: MazeGenerator generator of new lines

    Caution:
        Maze must be closed before Areas and paths are added.

    Example:

            ::

                maze = Maze(width=10)

                maze.grow(10)

                maze.close()

                <claim areas and paths>


                This is the same as

                maze = Maze(width=10, height=10)

                <claim areas and paths>
        
        

    """
    class Node:
        """Node holds identifier and coordinates

        Attributes:
            id: integer node identifier
            x: integer x coordinate
            y: integer y coordinate
        """
        def __init__(self, *, node_id=-1, x=-1, y=-1):
            self.id = node_id
            self.x = x
            self.y = y

    class Point:
        """Point holds coordinates

        Attributes:
            x: integer x coordinate
            y: integer y coordinate
        """
        def __init__(self, *, x=-1, y=-1):
            self.x = x
            self.y = y

    class Box:
        """Box holds dimensions

        Attribtues:
            width: integer, width of area
            hegiht: integer, height of area
        """
        def __init__(self, *, width=-1, height=-1):
            self.width = width
            self.height = height

    class Area:
        """Maze area

        A rectangular area that is assoicated with nodes in the maze

        Attributes:
            origin: A Maze.Point that is decomposed coordinates of a node id
            box: A Maze.Box holding dimensions of the area
            center: list of node identifiers that are not border nodes
            up_border: list of nodes ids on top border of the area
            down_border: list of nodes ids on bottom border of the area
            left_border: list of nodes ids on left border of the area
            right_border: list of nodes ids on right border of the area
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

    def __init__(self, *, width=MIN, height=None, maze_generator=Ellers):
        """Inits the maze with Ellers generator, a width of atleast 5 cells

        If height is defined, then a closed maze is constructed

        Raises:
            TypeError: maze_generator must be subclass of MazeGenerator
        """
        self.width = max(Maze.MIN, width)
        self.graph = nx.DiGraph()
        self.areas = {}
        self.is_closed = False
        assert issubclass(maze_generator, MazeGenerator),\
            f"Maze parameter maze_generator must be derived from MazeGenerator"
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
        """grows the maze by calling next on generator

        Args:
            line_count: integer specifying the number of lines to generate

        Returns:
            2-tuple with node list and edge list. ([0,1,2...], [(0, 1)...])
        """
        if self.graph.nodes():
            return [], []
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
        """Connects an areas nodes in a grid pattern

        Args:
            Area: Maze.Area
        """
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
            edges.extend([(node, Maze._apply_dir(self._maze.down, node)),
                          (Maze._apply_dir(self._maze.down, node), node)])
            edges.extend([(node, Maze._apply_dir(self._maze.up, node)),
                          (Maze._apply_dir(self._maze.up, node), node)])
            edges.extend([(node, Maze._apply_dir(self._maze.left, node)),
                          (Maze._apply_dir(self._maze.left, node), node)])
            edges.extend([(node, Maze._apply_dir(self._maze.right, node)),
                          (Maze._apply_dir(self._maze.right, node), node)])

        borders = [area.up_border, area.down_border,
                   area.left_border, area.right_border]
        for edge in borders:
            one_way = list(zip(edge, edge[1:]))
            edges.extend(one_way)
            other_way = [(v, u) for (u, v) in one_way]
            edges.extend(other_way)

        self.graph.add_edges_from(edges)

    @staticmethod
    def _apply_dir(dir_function, node):
        try:
            return dir_function(node)
        except IndexError:
            return None

    def _get_direction(self, nids, node):
        """Returns a valid node identifier from any direction from node

        Args:
            nids: node ids associated with the border of an area
            node: node identifier to offset from
        """
        possible = []

        possible = [Maze._apply_dir(self._maze.up, node),
                    Maze._apply_dir(self._maze.down, node),
                    Maze._apply_dir(self._maze.left, node),
                    Maze._apply_dir(self._maze.right, node)]
        return list(filter(lambda x: x not in nids and x, possible))[0]

    def _stitch_components(self, components):
        """Makes non area associated components fully connected

        When claiming an area, the graph can become split, breaking up paths
        between rooms. This funtion gets border nodes of each component and
        passes it to the combining function.

        Args:
            components: list of lists of node identifiers
        """
        borders = {id(component): Maze.Area() for component in components}
        nodes = []

        for component in components:
            for node in component:
                x, y = node % self.width, int(node / self.width)
                nodes.append(Maze.Node(node_id=node, x=x, y=y))

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
        """combines border nodes of components

        Attempts to combine components logically using maze directions

        Args:
            walls: list of lists of node identifiers that border components
        """
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
                    try:
                        possible_edges.extend([(candidate,
                                                getattr(self._maze,
                                                        inverse[direction])
                                                (candidate))
                                               for candidate in candidates if
                                               candidate in compare_to])
                    except IndexError:
                        pass
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
            node = Maze.Node(node_id=self._get_area_offset(area, dx, dy),
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

        Args:
            node_id_pair: a tuple of node identifiers

        Returns:
            A tuple with the node_id_pair and the distance
        """
        node_id1, node_id2 = node_id_pair[0], node_id_pair[1]
        x_1, y_1 = node_id1 % self.width, int(node_id1 / self.width)
        x_2, y_2 = node_id2 % self.width, int(node_id2 / self.width)
        return (node_id_pair, sqrt(pow((x_2-x_1), 2)+pow((y_2-y_1), 2)))

    def claim_area(self, name, area):
        """claims a set of nodes, makes maze consistent

        Once an area is claimed the maze graph can become disconnected,
        the function attempts to connect the maze using the coordinate
        system, but falls back to shortest distance if that fails.

        Args:
            name: Unique name for the area
            area: Maze.Area instance

        Raises:
            RuntimeWarning: maze needs to be closed
            KeyError: maze area with name was already claimed
            ValueError: area position or dimensions not valid for maze
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
        """generates path for two areas if possible

        Args:
            from_area_name: name as a string for the departing area
            from_way: direction as a string
            to_area_name: name as a string for the destination area
            to_way: direction as a string

        Returns:
            Empty list if no path is possible

            Tuple with the first and last elment being the arguments to the
            function and node identifiers as the path between them.

        Raises:
            RuntimeWarning: the maze should be closed before path generation
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
