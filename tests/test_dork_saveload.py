"""Tests saveload.
"""
from types import FunctionType
import dork.saveload


def testsave(run):
    """Save data should actually work no matter what
    type of data is used.
    """
    assert "main" in vars(dork.saveload), "Dork.cli should define a main method"
    assert isinstance(dork.saveload.main, FunctionType)
    try:
        run(dork.saveload.main, input_values=['basicmap'])
    except:  # noqa: E722
        raise AssertionError("cannot run 'dork' command")



def testload(run):
    """load should grab the data and parse it without further input
    """
    assert isinstance(dork.saveload.load, FunctionType)
    try:
        run(dork.saveload.load, input_values=['basicmap'])
    except:  # noqa: E722
        raise AssertionError("cannot run 'dork' command")
