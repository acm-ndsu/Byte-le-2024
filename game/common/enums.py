from enum import Enum, auto

"""
The use of the enum structure is to make is easier to execute certain tasks. It also helps with identifying 
types of Objects throughout the project. 

When developing the game, add any extra enums as necessary.
"""


class DebugLevel(Enum):
    NONE = auto()
    CLIENT = auto()
    CONTROLLER = auto()
    ENGINE = auto()


class ObjectType(Enum):
    NONE = auto()                           # 1
    ACTION = auto()                         # 2
    PLAYER = auto()                         # 3
    AVATAR = auto()                         # 4
    GAMEBOARD = auto()                      # 5
    VECTOR = auto()                         # 6
    TILE = auto()                           # 7
    WALL = auto()                           # 8
    ITEM = auto()                           # 9
    ORE = auto()                            # 10
    LAMBDIUM = auto()                       # 11
    TURITE = auto()                         # 12
    COPIUM = auto()                         # 13
    OCCUPIABLE = auto()                     # 14
    ANCIENT_TECH = auto()                   # 15
    STATION = auto()                        # 16
    OCCUPIABLE_STATION = auto()             # 17
    LAMBDIUM_OCCUPIABLE_STATION = auto()    # 18
    TURITE_OCCUPIABLE_STATION = auto()      # 19
    COPIUM_OCCUPIABLE_STATION = auto()      # 20
    STATION_EXAMPLE = auto()                # 21
    STATION_RECEIVER_EXAMPLE = auto()       # 22
    OCCUPIABLE_STATION_EXAMPLE = auto()     # 23
    ACTIVE_ABILITY = auto()                 # 24
    INVENTORY_MANAGER = auto()              # 25
    DYNAMITE_ACTIVE_ABILITY = auto()        # 26
    DYNAMITE = auto()                       # 27
    ORE_OCCUPIABLE_STATION = auto()         # 28
    TRAP = auto()                           # 29
    LANDMINE = auto()                       # 30
    EMP = auto()                            # 31


class ActionType(Enum):
    NONE = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    INTERACT_UP = auto()
    INTERACT_DOWN = auto()
    INTERACT_LEFT = auto()
    INTERACT_RIGHT = auto()
    INTERACT_CENTER = auto()
    PLACE_DYNAMITE = auto()
    PLACE_LANDMINE = auto()
    PLACE_EMP = auto()

# Added for Quarry Rush

class Company(Enum):
    CHURCH = auto()
    TURING = auto()
