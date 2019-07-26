"""tests types not covered in other test files
"""
import yaml
from dork.types import Map, Game


def dork_test_map():
    """tests map class
    """
    with open('./dork/yaml/default.yml') as file:
        data = yaml.safe_load(file.read())
    minimap = Map(Game(data))
    minimap.update()
