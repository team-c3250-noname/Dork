"""Tests for dork.Maze
"""
import networkx as nx
from dork.maze import MazeGenerator, Ellers, Maze

def test_maze_ellers():
    maze = Ellers()
    maze_gen = maze.generate()
    next(maze_gen)
    next(maze_gen)

    assert len(maze.nodes) == 4, f"Ellers should be minimum 4 nodes, 2 lines"

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
    
    maze.generate()

    assert len(maze.nodes)

    maze.open()
        

    maze.close()
       

    maze.get_nodes()

    maze.get_nodes_and_edges()

    maze.get_edges()
