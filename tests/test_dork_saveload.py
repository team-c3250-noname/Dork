"""Tests saveload.
"""
from types import FunctionType
import dork.saveload


def testsave(run):
    """Save data should actually work no matter what
    type of data is used.
    """
    assert isinstance(dork.saveload.save, FunctionType)
    try:
        run(dork.saveload.save, input_values=['basicmap'])
        run(dork.saveload.save, input_values=['\0', 'basicmap'])
    except:  # noqa: E722
        raise AssertionError("cannot run 'dork' command")


def testload(run):
    """load should grab the data and parse it without further input
    """
    assert isinstance(dork.saveload.load, FunctionType)
    try:
        run(dork.saveload.load, input_values=['basicmap'])
        run(dork.saveload.load, input_values=['\0', 'basicmap'])
    except:  # noqa: E722
        raise AssertionError("cannot run 'dork' command")
