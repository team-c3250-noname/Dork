#Dork

[![Build Status](https://travis-ci.com/team-c3250-noname/Dork.svg?branch=master)](https://travis-ci.com/team-c3250-noname/Dork)


    Dork is a game based on zork. A player can navigate through various rooms,
    pick up items, and using keys go to other areas. It currently has navigation
    and a command line interface, with repl and basic save and loading functions.





* Free software: MIT license
* Documentation:


Features
--------

* Added SonarCloud and TravisCI testing
* Command line interface with -h, -v, and -l options working
    * to-do: -o and -i for saving a map and initializing dork before start
* Dork start up menu
* REPL
    * Accepts [verb] [nown] sentences and navigates between rooms
* Save and load using YAML format
    * Can save rooms

*How do I:*
--------
    * Install
        1. Install python 3+, and git
        2. git clone https://github.com/team-c3250-noname/Dork.git
        3. pip install requirements-dev.txt and pip install requirements.txt
    * Run 
        1. python -m dork <options>
            * <no options> runs start menu
            * -h [--help] provide helpful message
            * -v [--version] outputs the version
            * -l [--list] outputs available mazes
        2. Playing the game
            * Start menu
                * quit - quits the game
                * load - loads room and item data
                * help - provides basic instructions
            * Select play
                * Follow the interactive prompt instructions, use "help"
                    * Some indicate what keywords to use
                    * Most follow <verb> <noun> structure
                * when done type in quit
        3. Developers
            * Currently the game consists of a single map with rooms, there are no development tools or tests.
        

TODO
---

* Map rooms onto maze generator
* Save map with rooms

Credits
-------

Please see the credits provided in the repo or Documentation.
