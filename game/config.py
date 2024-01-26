import os

from game.common.enums import *

"""
This file is important for configuring settings for the project. All parameters in this file have comments to explain 
what they do already. Refer to this file to clear any confusion, and make any changes as necessary.
"""

# Runtime settings / Restrictions --------------------------------------------------------------------------------------
# The engine requires these to operate
MAX_TICKS = 200                                     # max number of ticks the server will run regardless of game state
TQDM_BAR_FORMAT = "Game running at {rate_fmt} "     # how TQDM displays the bar
TQDM_UNITS = " turns"                               # units TQDM takes in the bar

MAX_SECONDS_PER_TURN = 0.2                          # max number of basic operations clients have for their turns

MAX_NUMBER_OF_ACTIONS_PER_TURN = 5                  # master_controller will be handling max actions enforcement for Byte-le 2024 "Quarry Rush"

MIN_CLIENTS_START = None                            # minimum number of clients required to start running the game; should be None when SET_NUMBER_OF_CLIENTS is used
MAX_CLIENTS_START = None                            # maximum number of clients required to start running the game; should be None when SET_NUMBER_OF_CLIENTS is used
SET_NUMBER_OF_CLIENTS_START = 2                     # required number of clients to start running the game; should be None when MIN_CLIENTS or MAX_CLIENTS are used
CLIENT_KEYWORD = "client"                           # string required to be in the name of every client file, not found otherwise
CLIENT_DIRECTORY = "./"                             # location where client code will be found

MIN_CLIENTS_CONTINUE = None                         # minimum number of clients required to continue running the game; should be None when SET_NUMBER_OF_CLIENTS is used
MAX_CLIENTS_CONTINUE = None                         # maximum number of clients required to continue running the game; should be None when SET_NUMBER_OF_CLIENTS is used
SET_NUMBER_OF_CLIENTS_CONTINUE = 2                  # required number of clients to continue running the game; should be None when MIN_CLIENTS or MAX_CLIENTS are used

# Game Variables
# Ore Count on game board (referenced in collectable_generator.py)
ORE_COUNT = 100                                     # Number of ores generated on the game board for a game

# Dynamite (referenced in dynamite.py and dynamite_active_ability.py)
DYNAMITE_FUSE = 2                                   # Number of turns before dynamite item explodes
DYNAMITE_COOLDOWN = 3                               # Number of turns player waits before they can activate the Dynamite ability again

# Landmine (referenced in traps.py and landmine_active_ability.py)
LANDMINE_STEAL_RATE = 0.5                           # Chance to steal each item in opponents inventory when Landmine detonates
LANDMINE_COOLDOWN = 4                               # Number of turns player waits before they can activate the Landmine ability again
LANDMINE_RANGE = 1                                  # Range for detonation of a landmine

# EMP (referenced in traps.py and emp_active_ability.py)
EMP_STEAL_RATE = 1.0                                # Chance to steal each item in opponents inventory when EMP detonates
EMP_COOLDOWN = 4                                    # Number of turns player waits before they can activate the EMP ability again
EMP_RANGE = 2                                       # Range for detonation of a EMP

# Trap Defusal (referenced in trap_defusal_active_ability)
TRAP_DEFUSAL_COOLDOWN = 2                           # Number of turns player waits before they can activate the Trap Defusal ability again
TRAP_DEFUSAL_RANGE = EMP_RANGE + 1                  # Range for defusing traps on the map

# Tech Costs (referenced in tech.py)
IMPROVED_DRIVETRAIN_COST = 80                       # Cost of the Improved Drivetrain tech
SUPERIOR_DRIVETRAIN_COST = 160                      # Cost of the Superior Drivetrain tech
OVERDRIVE_DRIVETRAIN_COST = 320                     # Cost of the Overdrive Drivetrain tech
IMPROVED_MINING_COST = 50                           # Cost of the Improved Mining tech
SUPERIOR_MINING_COST = 100                          # Cost of the Superior Mining tech
OVERDRIVE_MINING_COST = 200                         # Cost of the Overdrive Mining tech
DYNAMITE_COST = 70                                  # Cost of the Dynamit tech
LANDMINE_COST = 120                                 # Cost of the Landmine tech
EMP_COST = 180                                      # Cost of the EMP tech
TRAP_DEFUSAL_COST = 180                             # Cost of the Trap Defusal tech

# Tech Points (referenced in tech.py)
IMPROVED_DRIVETRAIN_POINTS = 150                    # Points awarded when purchasing the Improved Drivetrain tech
SUPERIOR_DRIVETRAIN_POINTS = 250                    # Points awarded when purchasing the Superior Drivetrain tech
OVERDRIVE_DRIVETRAIN_POINTS = 350                   # Points awarded when purchasing the Overdrive Drivetrain tech
IMPROVED_MINING_POINTS = 100                        # Points awarded when purchasing the Improved Mining tech
SUPERIOR_MINING_POINTS = 150                        # Points awarded when purchasing the Superior Mining tech
OVERDRIVE_MINING_POINTS = 300                       # Points awarded when purchasing the Overdrive Mining tech
DYNAMITE_POINTS = 140                               # Points awarded when purchasing the Dynamite tech
LANDMINE_POINTS = 240                               # Points awarded when purchasing the Landmine tech
EMP_POINTS = 360                                    # Points awarded when purchasing the EMP tech
TRAP_DEFUSAL_POINTS = 360                           # Points awarded when purchasing the Trap Defusal tech


ALLOWED_MODULES = ["game.client.user_client",       # modules that clients are specifically allowed to access
                   "game.common.enums",
                   "game.common.map.game_board",
                   "game.common.map.tile",
                   "game.common.map.wall",
                   "game.common.map.game_board",
                   "game.common.avatar",
                   "game.common.items.item",
                   "game.common.stations.station",
                   "game.common.stations.occupiable_station",
                   "game.utils.vector",
                   "game.quarry_rush.entity.placeable.dynamite",
                   "game.quarry_rush.entity.placeable.traps",
                   "game.quarry_rush.entity.ancient_tech",
                   "game.quarry_rush.entity.ores",
                   "game.quarry_rush.station.company_station",
                   "game.quarry_rush.station.ore_occupiable_station",
                   "typing",
                   "numpy",
                   "scipy",
                   "pandas",
                   "itertools",
                   "functools",
                   "random",
                   "heapq",
                   "sympy",
                   ]

RESULTS_FILE_NAME = "results.json"                                  # Name and extension of results file
RESULTS_DIR = os.path.join(os.getcwd(), "logs")                     # Location of the results file
RESULTS_FILE = os.path.join(RESULTS_DIR, RESULTS_FILE_NAME)         # Results directory combined with file name

LOGS_FILE_NAME = 'turn_logs.json'
LOGS_DIR = os.path.join(os.getcwd(), "logs")                        # Directory for game log files
LOGS_FILE = os.path.join(LOGS_DIR, LOGS_FILE_NAME)

GAME_MAP_FILE_NAME = "game_map.json"                                # Name and extension of game file that holds generated world
GAME_MAP_DIR = os.path.join(os.getcwd(), "logs")                    # Location of game map file
GAME_MAP_FILE = os.path.join(GAME_MAP_DIR, GAME_MAP_FILE_NAME)      # Filepath for game map file


class Debug:                    # Keeps track of the current debug level of the game
    level = DebugLevel.NONE

# Other Settings Here --------------------------------------------------------------------------------------------------
