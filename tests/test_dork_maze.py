"""Tests for dork.Maze
"""
import networkx as nx
from dork.maze import Ellers, Maze


def test_maze_ellers(mocker):
    """tests the ellers maze generator
    """
    def join_replace():
        return 0

    def vert(line):
        return [line]

    line_count = 10
    maze = Ellers(width=line_count)
    maze_gen = maze.generate()
    for _ in range(0, line_count):
        next(maze_gen)
    maze.close()

    graph = nx.DiGraph()
    graph.add_nodes_from(maze.get_nodes())
    graph.add_edges_from(maze.get_edges())
    assert nx.is_strongly_connected(graph),\
        f"generated mazes should be fully connected"

    setattr(Ellers, "_should_join", join_replace)
    maze = Ellers(width=2)

    mocker.patch.object(maze, "_random_vertical_nodes", vert)
    maze_generator = maze.generate()
    next(maze_generator)

    try:
        maze.get_nodes()
    except RuntimeWarning as warning:
        assert "close" in str(warning),\
            f"get_nodes should warn against open mazes"
    try:
        maze.get_edges()
    except RuntimeWarning as warning:
        assert "close" in str(warning),\
            f"get_nodes should warn against open mazes"
    try:
        maze.get_nodes_and_edges()
    except RuntimeWarning as warning:
        assert "close" in str(warning),\
            f"get_nodes should warn against open mazes"

    maze.close()

    assert next(maze_generator) is None, f"closed mazes should return None"

    assert len(maze.nodes) == 4, f"Ellers should be minimum 4 nodes, 2 lines"
    assert len(maze.get_nodes()) == 4, f"Ellers should be minimum 4 nodes"
    assert maze.get_edges() is maze.edges and maze.edges is not None,\
        f"get edges is either not returning edge list or edge list is none"
    assert len(maze.get_nodes_and_edges()) == 2,\
        f"should return node and edge list in a tuple"

    assert maze.up(2) == 0, f"Ellers up from 2 should have been 0"

    assert maze.up(0) is None, f"Eller up from top line should be None"
    assert maze.up(1) is None, f"Eller up from top line should be None"

    assert maze.down(2) is None, f"Ellers down from bottom edge should be none"
    assert maze.down(3) is None, f"Ellers down from bottom edge should be none"

    assert maze.left(0) is None, f"Ellers left from left edge should be None"
    assert maze.left(2) is None, f"Ellers left from left edge should be None"

    assert maze.right(1) is None,\
        f"Ellers right from right edge should be None"
    assert maze.right(3) is None,\
        f"Ellers right from right edge should be None"

    graph = nx.DiGraph()
    graph.add_nodes_from(maze.get_nodes())
    graph.add_edges_from(maze.get_edges())
    assert nx.is_strongly_connected(graph),\
        f"generated mazes should be fully connected"


def test_maze_maze():
    """tests maze initialization
    """
    try:
        maze = Maze(filename="test.yaml")
        maze = maze
    except NotImplementedError as err:
        assert "save load" in str(err), f"maze filename save load not done"

    maze = Maze(width=5)
    maze.grow(4)
    try:
        maze.size()
    except RuntimeWarning as err:
        assert "closed" in str(err), f"maze should be read only until closed"
    try:
        maze.get_path("", "", "", "")
    except RuntimeWarning as err:
        assert "closed" in str(err), f"maze should be read only until closed"
    try:
        maze.claim_area("", None)
    except RuntimeWarning as err:
        assert "closed" in str(err), f"maze should be read only until closed"

    maze.close()

    assert maze.size() == 25, f"maze should have 25 nodes"
    assert maze.grow() == (None, None), f"closed maze should not grow"


def test_maze_claim_area():
    """tests maze claim area
    """
    maze = Maze(width=10, height=10)
    maze.claim_area("room", Maze.Area(x=0, y=0, width=2, height=2))

    assert maze.areas["room"], f"room was not found after claimed"

    try:
        maze.claim_area("room", Maze.Area(x=0, y=0, width=2, height=2))
    except KeyError as err:
        assert "already used" in str(err), f"area should of been claimed"

    try:
        maze.claim_area("test", Maze.Area(x=0, y=0, width=1000, height=2))
    except ValueError as err:
        assert "too large" in str(err), f"width was too large for maze"

    try:
        maze.claim_area("test", Maze.Area(x=-1, y=0, width=1000, height=2))
    except ValueError as err:
        assert "positive" in str(err), f"area properties are only positive"

    maze = Maze(width=10, height=10)
    maze.claim_area("hallway", Maze.Area(x=3, y=0, width=3, height=1))
    assert "hallway" in maze.areas, f"hallway was not found in maze"


def test_maze_get_path():
    """tests maze get path
    """
    maze = Maze(width=10, height=10)
    maze.claim_area("room", Maze.Area(x=0, y=0, width=2, height=2))
    maze.claim_area("hallway", Maze.Area(x=3, y=0, width=3, height=1))
    maze.claim_area("big_room", Maze.Area(x=3, y=3, width=3, height=3))

    path = maze.get_path("room", "right", "hallway", "left")
    assert "room" in path[0][0], f"room from path should start from room"
    assert "hallway" in path[-1][0], f"path should end at hallway"
