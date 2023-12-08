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
    NONE = auto()  # 1
    ACTION = auto()  # 2
    PLAYER = auto()  # 3
    AVATAR = auto()  # 4
    GAMEBOARD = auto()  # 5
    VECTOR = auto()  # 6
    TILE = auto()  # 7
    WALL = auto()  # 8
    ITEM = auto()  # 9
    ORE = auto()  # 10
    LAMBDIUM = auto()  # 11
    TURITE = auto()  # 12
    COPIUM = auto()  # 13
    OCCUPIABLE = auto()  # 14
    ANCIENT_TECH = auto()  # 15
    STATION = auto()  # 16
    OCCUPIABLE_STATION = auto()  # 17
    STATION_EXAMPLE = auto()  # 18
    STATION_RECEIVER_EXAMPLE = auto()  # 19
    OCCUPIABLE_STATION_EXAMPLE = auto()  # 20
    COMPANY_STATION = auto()  # 21
    CHURCH_STATION = auto()  # 22
    TURING_STATION = auto()  # 23
    ACTIVE_ABILITY = auto()  # 24
    INVENTORY_MANAGER = auto()  # 25
    PLACE_TRAP = auto()  # 26
    DYNAMITE_ACTIVE_ABILITY = auto()  # 27
    DYNAMITE = auto()  # 28
    ORE_OCCUPIABLE_STATION = auto()  # 29
    ANCIENT_TECH_OCCUPIABLE_STATION = auto()  # 30
    TRAP = auto()  # 31
    LANDMINE = auto()  # 32
    EMP = auto()  # 33


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
    MINE = auto()
    DEFUSE_UP = auto()
    DEFUSE_DOWN = auto()
    DEFUSE_LEFT = auto()
    DEFUSE_RIGHT = auto()


# Added for Quarry Rush
class Company(Enum):
    CHURCH = auto()
    TURING = auto()
