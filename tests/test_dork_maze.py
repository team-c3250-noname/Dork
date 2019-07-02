"""Tests for dork.Maze
"""
from os import linesep
import networkx as nx
from dork.maze import MazeGenerator, Ellers, Maze


def test_dork_maze():
    """Tests the dork.Maze class
    """
    maze = Maze()
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
    