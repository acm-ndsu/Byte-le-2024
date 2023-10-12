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
    NONE = auto()                               # 1
    ACTION = auto()                             # 2
    PLAYER = auto()                             # 3
    AVATAR = auto()                             # 4
    GAMEBOARD = auto()                          # 5
    VECTOR = auto()                             # 6
    TILE = auto()                               # 7
    WALL = auto()                               # 8
    ITEM = auto()                               # 9
    ORE = auto()                                # 10
    LAMBDIUM = auto()                           # 11
    TURITE = auto()                             # 12
    COPIUM = auto()                             # 13
    OCCUPIABLE = auto()                         # 14
    ANCIENT_TECH = auto()                       # 15
    STATION = auto()                            # 16
    OCCUPIABLE_STATION = auto()                 # 17
    LAMBDIUM_OCCUPIABLE_STATION = auto()        # 18
    TURITE_OCCUPIABLE_STATION = auto()          # 19
    COPIUM_OCCUPIABLE_STATION = auto()          # 20
    STATION_EXAMPLE = auto()                    # 21
    STATION_RECEIVER_EXAMPLE = auto()           # 22
    OCCUPIABLE_STATION_EXAMPLE = auto()         # 23
    COMPANY_STATION = auto()                    # 24
    CHURCH_STATION = auto()                     # 25
    TURING_STATION = auto()                     # 26
    ACTIVE_ABILITY = auto()                     # 27
    INVENTORY_MANAGER = auto()                  # 28
    DYNAMITE_ACTIVE_ABILITY = auto()            # 29
    DYNAMITE = auto()                           # 30
    ORE_OCCUPIABLE_STATION = auto()             # 31
    ANCIENT_TECH_OCCUPIABLE_STATION = auto()    # 32
    TRAP = auto()                               # 33
    LANDMINE = auto()                           # 34
    EMP = auto()                                # 35


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
    SELECT_SLOT_0 = auto()
    SELECT_SLOT_1 = auto()
    SELECT_SLOT_2 = auto()
    SELECT_SLOT_3 = auto()
    SELECT_SLOT_4 = auto()
    SELECT_SLOT_5 = auto()
    SELECT_SLOT_6 = auto()
    SELECT_SLOT_7 = auto()
    SELECT_SLOT_8 = auto()
    SELECT_SLOT_9 = auto()
    """
    These last 10 enums are for selecting a slot from the Avatar class' inventory.
    You can add/remove these as needed for the purposes of your game. 
    """


# Added for Quarry Rush

class Company(Enum):
    CHURCH = auto()
    TURING = auto()
