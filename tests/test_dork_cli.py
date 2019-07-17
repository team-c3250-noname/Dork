# -*- coding: utf-8 -*-
"""Basic tests for the dork cli
"""
from types import FunctionType
import dork.cli


def test_cli_exists(run):
    """Dork.cli.main should always exist and run
    """
    assert "main" in vars(dork.cli), "Dork.cli should define a main method"
    assert isinstance(dork.cli.main, FunctionType)
    try:
        run(dork.cli.main)
        run(dork.cli.main, input_values=['jump', ' ', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', ' ', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'save',
                                         'roomdatatest', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'jump high',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'move north',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'move south',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'move west',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'move east',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'move qest',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'examine room',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default',
                                         'examine nothing', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick cellkey',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'examine room', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'move north', 'use key', 'south',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'use key', 'qest', 'south',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'move north', 'use key',
                                         'north', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'examine key', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'use key', 'north', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'use key', 'north', 'move north',
                                         'punch',
                                         'pick torch', 'use torch',
                                         'west', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'use key', 'north', 'move north',
                                         'swing',
                                         'pick torch', 'use torch',
                                         'west', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'pick skull',
                                         'use key', 'north', 'move north',
                                         'swing', 'skull',
                                         'pick torch', 'use torch',
                                         'west', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'pick skull',
                                         'use key', 'north', 'move north',
                                         'swing', 'grenade', 'skull',
                                         'pick torch', 'use torch',
                                         'west', 'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'user inventory',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'user save',
                                         'quit'])
        run(dork.cli.main, input_values=['play', 'default', 'user id',
                                         'quit'])
        run(dork.cli.main, input_values=['load', 'default', ' ', 'quit'])
        run(dork.cli.main, input_values=['help', ' ', 'quit'])
        run(dork.cli.main, input_values=['quit'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'use key', 'north', 'move north',
                                         'punch',
                                         'pick torch', 'use torch',
                                         'right', 'move right', 'move up',
                                         'punch',
                                         'pick bar', 'move down',
                                         'move down', 'use bar', 'left',
                                         'move left', 'punch', 'pick sword',
                                         'move north', 'swing', 'sword',
                                         'move north'])
        run(dork.cli.main, input_values=['play', 'default', 'pick key',
                                         'use key', 'north', 'move north',
                                         'punch',
                                         'pick torch', 'use torch',
                                         'right', 'move right', 'move up',
                                         'punch',
                                         'pick bar', 'move down',
                                         'move down', 'use bar', 'left',
                                         'move left', 'punch', 'pick sword',
                                         'move north', 'punch',
                                         'move north'])
    except:  # noqa: E722
        raise AssertionError("cannot run 'dork' command")


def test_cli_help(run):
    """CLI's help command should return helpful information
    """
    msg = []
    _, err = run(dork.cli.the_predork_cli, msg, *("", "-h"))
    assert "usage: " in msg[0], \
        "Failed to run the cli.main method: {err}".format(err=err)


def test_pre_cli_version(run):
    """version should print dork.__version__
    """
    out, err = run(dork.cli.the_predork_cli, [], *("", "-v"))
    assert dork.__version__ in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)


def test_pre_cli_list(run):
    """dork cli -l option should list test.drk file
    """
    out, err = run(dork.cli.the_predork_cli, [], *("", "-l"))
    assert "test.yml" in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)


def test_pre_cli_list_version(run):
    """tests both list and version
    """
    out, err = run(dork.cli.the_predork_cli, [], *("", "-l", "-v"))
    assert "test.yml" in out and dork.__version__ in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)


def test_pre_cli_init(run):
    """init should load given file or print not found message
    """
    out, err = run(dork.cli.the_predork_cli, [], *("", "-i", "test"))
    assert "test" in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)
    out, err = run(dork.cli.the_predork_cli, [], *("", "-i", ":test"))
    assert "does not exist" in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)


def test_pre_cli_generation(run):
    """pre_cli with -o generates a maze and then runs dork
    """
    out, err = run(dork.cli.the_predork_cli, [], *("", "-o", "test"))
    assert "saved" in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)
    out, err = run(dork.cli.the_predork_cli, [], *("", "-o", ":test"))
    assert "filenames" in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)
    out, err = run(dork.cli.the_predork_cli, [], *("", "-o", "test."))
    assert "Filenames" in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)
    out, err = run(dork.cli.the_predork_cli, [], *("", "-o", "CON"))
    assert "OS reserved" in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)
    out, err = run(dork.cli.main, [], *("", "noop"))
    assert "usage" in out, \
        "Failed run the dork.cli.the_predork_cli method: {err}"\
        .format(err=err)
