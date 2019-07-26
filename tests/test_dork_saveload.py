"""Tests saveload.
"""
from types import FunctionType
import yaml
import dork.saveload
from dork import types


def testsave(maptype, run):
    """Save data should actually work no matter what
    type of data is used.
    """
    assert isinstance(dork.saveload.save, FunctionType)
    try:
        with open('./dork/yaml/default.yml') as file:
            # Should not call load directly
            data = yaml.safe_load(file.read())

        game = types.Game(data)
        run(dork.saveload.save, game, input_values=['roomdatatest'])
        run(dork.saveload.save, game, input_values=['default', 'roomdatatest'])
        run(dork.saveload.save, game, input_values=['\0', 'roomdatatest'])
    except:  # noqa: E722
        raise AssertionError("cannot run 'dork' command")


def testload(maptype, run):
    """load should grab the data and parse it without further input
    """
    assert isinstance(dork.saveload.load, FunctionType)
    try:
        run(dork.saveload.load, input_values=['default'])
        run(dork.saveload.load, input_values=['\0', 'default'])
    except:  # noqa: E722
        raise AssertionError("cannot run 'dork' command")
