"""Tests for dork.Maze
"""
from os import linesep
import networkx as nx
from dork.maze import MazeGenerator, Ellers, Maze

MAZE = Maze()


def test_dork_maze(maze=MAZE):
    """Tests the dork.Maze class
    """
    graph = maze.get_graph()
    assert len(graph.nodes) == 110, f"Default node size was incorrect"
    assert nx.is_strongly_connected(graph),\
        f"Maze graph is not connected, not a maze"

    node = MazeGenerator.Node()
    assert node.id == 110, f"Node id not unique"
    assert node.__str__() == "110:-> -> -> -> ", f"node str failed"

    line = Ellers.Line(2)
    assert line.__str__() == "111:-> -> -> -> " + linesep + "112:-> -> -> -> "

    maze.maze_generator.close()
    assert next(maze.maze_generator.generate()) is None,\
        f"closed maze generator should return None"
    maze.maze_generator.open()
    assert next(maze.maze_generator.generate()) is not None,\
        f"opened maze, generator should not return None"

    try:
        maze = Maze(maze_generator=object)
    except TypeError as err:
        assert "derived" in str(err),\
            "Maze should not allow a maze_generator" + \
            " not derived from MazeGenerator"

    node_left = MazeGenerator.Node()
    node = MazeGenerator.Node()
    node_right = MazeGenerator.Node()

    node.set_left_right(node_left, 1000)
    assert node.left is node_left.id, f"node_left should be node.left"

    node.set_left_right(node_right, 1000)
    assert node.right is node_right.id, f"node_right should be node.right"

    node_left = MazeGenerator.Node()
    node = MazeGenerator.Node()
    node_right = MazeGenerator.Node()

    node.set_left_right(node_right, node_right.id+1)
    assert node.right is node_right.id, f"edge case, node.right failed"

    node.set_left_right(node_left, node_left.id)
    assert node.left is node_left.id, f"edge case, node.left failed"


def test_dork_maze_areas(maze=MAZE):
    """tests the area/room-map for maze
    """
    maze.claim_cell("c1", 0, 0)
    try:
        maze.claim_cell("c1", 0, 0)
    except KeyError as err:
        assert "already used" in str(err), f"claim_cell key duplication"

    try:
        maze.claim_cell("c2", -1, 0)
    except IndexError as err:
        assert "out of bounds" in str(err),\
                f"claim_cell does not allow negative indices"

    try:
        maze.claim_cell("c2", 0, 0)
    except ValueError as err:
        assert "already claimed" in str(err),\
                f"cell was already claimed"
    maze.claim_cell("c2", 4, 4)
    maze.make_path("c1", "down", "c2", "up")
    try:
        maze.make_path("c1", "left", "c2", "right")
    except ValueError as err:
        assert "cannot go" in str(err), f"tried to go left at 0,0"

    maze.make_path("c1", "right", "c2", "down")

    try:
        maze.make_path("c1", "up", "c2", "down")
    except ValueError as err:
        assert "cannot go" in str(err), f"tried to up at 0"
