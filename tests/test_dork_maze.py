"""Tests for dork.Maze
"""
from os import linesep
import networkx as nx
import pylab as plt
from dork.maze import MazeGenerator, Ellers, Maze

def get_maze():
    def _new_join():
        join_list = [0, 0, 0, 0, 0]
        n = len(join_list)
        i = 0
        while True:
            yield join_list[i % n]
            i += 1

    def _new_down_nodes(line):
        seen = {}
        down_indices = []
        for group in line.sets:
            if id(line.sets[group]) not in seen:
                population = line.sets[group]
                current_line_set = set(line.nodes)
                population = population.intersection(current_line_set)
                node_sample = [list(population)[0]]
                down_indices.append(node_sample)
                seen[id(line.sets[group])] = None
        return down_indices

    MazeGenerator.Node.ID = 0
    Ellers._should_join = _new_join
    Ellers._get_down_nodes = _new_down_nodes
    maze = Maze(Ellers, 5, 5)

    while True:
        yield maze


def test_dork_maze():
    """Tests the dork.Maze class
    """
    try:
        maze = Maze(object)
    except TypeError as err:
        assert "MazeGenerator" in str(err), f"Maze is not checking for MazeGenerator Abstract base class"
    maze = next(get_maze())

    assert isinstance(maze.get_graph(), nx.DiGraph), f"maze graph should be a digraph"

    assert len(maze.get_graph().nodes()) == 25, f"test maze should be 25 nodes"

    maze.maze_generator.close()
    assert next(maze.maze_generator.generate()) == None, f"maze generator closed?"
    maze.maze_generator.open()

    _, y = maze._get_node_way(0, "up")
    assert y == -1, f"Up should have subtracted from y coord"
    _, y = maze._get_node_way(0, "down")
    assert y == 1, f"down should have added from y coord"
    x, _ = maze._get_node_way(0, "left")
    assert x == -1, f"left should have subtracted from x coord"
    x, _ = maze._get_node_way(0, "right")
    assert x == 1, f"right should have added from x coord"

    



def test_dork_maze_areas():
    """tests the area/room-map for maze
    """
    maze = next(get_maze())

    maze.claim_cell("t0", 0, 0)
    maze.claim_cell("t1", 1, 0)
    maze.claim_cell("t2", 0, 1)
    maze.claim_cell("t3", 1, 1)
    maze.claim_cell("t4", 4, 2)
    maze.claim_cell("t5", 4, 0)
    maze.claim_cell("t6", 4, 3)
    maze.claim_cell("t7", 4, 4)
    maze.claim_cell("t8", 2, 1)
    maze.claim_cell("t9", 3, 1)
    
    maze.make_path("t0", "right", "t1", "left")
    maze.make_path("t1", "down", "t3", "up")
    maze.make_path("t5", "down", "t4", "up")
    maze.make_path("t6", "down", "t7", "up")
    maze.make_path("t8", "right", "t9", "left")

    assert maze.get_path("t0", "right") == [1, 0], f"wrong path"

    try:
        maze.claim_cell("t0", 0, 0)
    except KeyError as err:
        assert "already used for cell" in str(err), f"name t0 already used"
    
    try:
        maze.claim_cell("noop", 10, 10)
    except IndexError as err:
        assert "out of bounds" in str(err), f"index should have been out of bounds"
    try:
        maze.claim_cell("noop", 0, 0)
    except ValueError as err:
        assert "already claimed" in str(err), f"node was already claimed"
    
    try:
        maze.make_path("t0", "left", "t1", "down")
    except ValueError as err:
        assert "cannot go" in str(err), f"room should not have been formed."
    try:
        maze.make_path("t0", "up", "t1", "down")
    except ValueError as err:
        assert "cannot go" in str(err), f"room should not have been formed."
    
    maze.grow(10)
    assert len(maze.graph.nodes())==70, f"maze should have grown by 50 nodes"

    n = maze.maze_generator.Node()
    n_right = maze.maze_generator.Node()
    n.set_left_right(n_right, 5)
    assert n.right == n_right.id, f"n_right should be for n.right"
    
    