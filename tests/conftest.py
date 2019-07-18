# -*- coding: utf-8 -*-
"""Pytest Fixtures for Dork unit-tests
"""
import pytest
import dork.types as types

pytest_plugins = ["pytester"]  # pylint: disable=invalid-name


@pytest.fixture
def player():
    """A basic dork player fixture
    """
    return types.Player(types.GAME)


@pytest.fixture
def room():
    """A basic dork room fixture
    """
    return types.Room(types.GAME)


@pytest.fixture
def run(mocker, capsys):
    """CLI run method fixture
    """

    def do_run(main, *args, **kwargs):

        mocked_input = mocker.patch('builtins.input')
        mocked_input.side_effect = kwargs.get('input_values', ['quit'] * 100)
        main(*args)
        cap = capsys.readouterr()
        return cap.out, cap.err

    return do_run
