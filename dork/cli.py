# -*- coding: utf-8 -*-
"""Basic CLI Dork.
"""

import argparse
import os
import time
from io import StringIO
import cursor
import dork
import re


__all__ = ["main"]


def is_filename_compliant(filename):
    """checks if filename follows win and unix naming guidelines
       https://docs.microsoft.com/en-us/windows/desktop/FileIO/naming-a-file
       added in NULL character as well
    """
    if re.match(r'<|>|:|"|\/|\\|\||\?|\*|\0', filename):
        print(r"filenames cannot contain <, >, :, /, \|, ?, *")
        return False
    match = r'^((CON)|(PRN)|(AUX)|(NUL)|(COM)\d{1}|(LPT)\d{1})\.*(\w{3})*$'
    if re.match(match, filename):
        print("Filename cannot be a OS reserved name")
        return False
    if re.match(r'^.*( |\.)$', filename):
        print("Filenames should not end with space or period")
        return False
    return True

def the_predork_cli(help_msg, *args):
    """non-game loop command line """
    version = dork.__version__
    parser = argparse.ArgumentParser(description="Dork command line " +
                                     "interface. Run dork with no options to" +
                                     " begin game")

    parser.add_argument('-l', '--list', action='store_true',
                        help='list available mazes')
    parser.add_argument('-i', '--init',
                        help='-i <mazename> initializes dork with mazename')
    parser.add_argument('-o', '--out',
                        help='-o <mazename> generates a maze and saves it')
    parser.add_argument('-v', '--version', action='store_true',
                        help="prints version and exits")
    arglist = None

    _hf = StringIO()
    parser.print_usage(file=_hf)
    help_msg.append(_hf.getvalue())
    _hf.close()

    try:
        arglist, unkown_args = parser.parse_known_args(args[1:])
    except SystemExit:
        if "-h" in args or "--help" in args:
            return True
        print("Unrecognized commands")
        return True

    if "-h" in args or "--help" in args or unkown_args:
        return True

    if arglist.out:
        if not is_filename_compliant(arglist.out):
            return True

        _f = open("mazes/"+arglist.out+".drk", "w")
        cursor.hide()
        time.sleep(0.5)
        dots = ("Generating maze    ", "Generating maze .",
                "Generating maze ..", "Generating maze ...")
        for _t in range(20):
            print("{}".format(dots[_t % 4]), end="\r")
            time.sleep(1)
        print("{}".format(" "*len(dots[-1])))
        cursor.show()
        print("Done, maze \""+arglist.out+"\" saved")
        _f.close()

    if arglist.version:
        print(version)

    if arglist.list or arglist.init:
        mazes = []
        for (_, _, filenames) in os.walk("mazes/"):
            mazes.extend(filenames)
        only_maze_files = [maze for maze in mazes if maze.find(".drk") > 0]
        if arglist.list:
            print(os.linesep.join(only_maze_files))
        if arglist.init and arglist.init + ".drk" in only_maze_files:
            print("loaded maze "+arglist.init)
        elif arglist.init:
            print("maze "+arglist.init+" does not exist")

    return False


def main(*args):
    """Main CLI runner for Dork
    """
    help_msg = []

    arg_len = len(args)
    if arg_len == 1:
        print("running dork")

    if the_predork_cli(help_msg, *args):
        print(help_msg[0])
