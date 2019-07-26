import yaml
import pylab as plt
from dork.types import Map, Game, Room
import dork.saveload
from pytest_mock import mocker

def dork_test_map(maptype):
    with open('./dork/yaml/default.yml') as file:
        data = yaml.safe_load(file.read())
    minimap = Map(Game(data))