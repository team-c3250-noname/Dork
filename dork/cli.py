# -*- coding: utf-8 -*-
"""Basic CLI Dork.
"""

import argparse
import os
import time
import cursor

__all__ = ["in"]

def the_predork_cli(*args, version):
    """non-game loop command line """

    parser = argparse.ArgumentParser(description='Dork command line interface')

    parser.add_argument('-l', '--list', action='store_true', \
                        help='list available mazes')
    parser.add_argument('-i', '--init', \
                        help='-i <mazename> initializes dork with mazename')
    parser.add_argument('-o', '--out', \
                        help='-o <mazename> generates a maze and saves it')
    parser.add_argument('-v', '--version', action='store_true', \
                        help="prints version and exits")

    arglist = parser.parse_args(args[1:])

    run_flag = False

    if arglist.out:
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
        run_flag = True

    if arglist.version:
        print("Dork version --> " + version)
        run_flag = True

    if arglist.list or arglist.init:
        mazes = []
        for (_, _, filenames) in os.walk("mazes/"):
            mazes.extend(filenames)
        only_maze_files = [maze for maze in mazes if maze.find(".drk") > 0]
        if arglist.list:
            print(os.linesep.join(only_maze_files))
            run_flag = True
        if arglist.init:
            arglist.init = arglist.init + ".drk"
            if arglist.init in only_maze_files:
                print("loaded maze "+arglist.init)
            else:
                print("maze "+arglist.init+" does not exist")
            run_flag = False


    return run_flag

def main(*args):
    """Main CLI runner for Dork
    """

    if not the_predork_cli(*args, version="0.0.1"):
        print("running dork")
