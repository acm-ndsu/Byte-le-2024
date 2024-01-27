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
    LANDMINE_ACTIVE_ABILITY = auto()  # 26
    EMP_ACTIVE_ABILITY = auto()  # 27
    DYNAMITE_ACTIVE_ABILITY = auto()  # 28
    DYNAMITE = auto()  # 29
    ORE_OCCUPIABLE_STATION = auto()  # 30
    TRAP = auto()  # 31
    LANDMINE = auto()  # 32
    EMP = auto()  # 33
    TRAP_DEFUSAL_ACTIVE_ABILITY = auto()  # 34


class ActionType(Enum):
    NONE = auto()  # 1
    MOVE_UP = auto()  # 2
    MOVE_DOWN = auto()  # 3
    MOVE_LEFT = auto()  # 4
    MOVE_RIGHT = auto()  # 5
    INTERACT_UP = auto()  # 6
    INTERACT_DOWN = auto()  # 7
    INTERACT_LEFT = auto()  # 8
    INTERACT_RIGHT = auto()  # 9
    INTERACT_CENTER = auto()  # 10
    PLACE_DYNAMITE = auto()  # 11
    PLACE_LANDMINE = auto()  # 12
    PLACE_EMP = auto()  # 13
    MINE = auto()  # 14
    DEFUSE = auto()  # 15
    BUY_IMPROVED_DRIVETRAIN = auto()  # 16
    BUY_SUPERIOR_DRIVETRAIN = auto()  # 17
    BUY_OVERDRIVE_DRIVETRAIN = auto()  # 18
    BUY_IMPROVED_MINING = auto()  # 19
    BUY_SUPERIOR_MINING = auto()  # 20
    BUY_OVERDRIVE_MINING = auto()  # 21
    BUY_DYNAMITE = auto()  # 22
    BUY_LANDMINES = auto()  # 23
    BUY_EMPS = auto()  # 24
    BUY_TRAP_DEFUSAL = auto()  # 25


# Added for Quarry Rush
class Company(Enum):
    CHURCH = auto()  # 1
    TURING = auto()  # 2

class Tech(Enum):
    IMPROVED_DRIVETRAIN = 'Improved Drivetrain'
    SUPERIOR_DRIVETRAIN = 'Superior Drivetrain'
    OVERDRIVE_DRIVETRAIN = 'Overdrive Drivetrain'
    IMPROVED_MINING = 'Improved Mining'
    SUPERIOR_MINING = 'Superior Mining'
    OVERDRIVE_MINING = 'Overdrive Mining'
    DYNAMITE = 'Dynamite'
    LANDMINES = 'Landmines'
    EMPS = 'EMPs'
    TRAP_DEFUSAL = 'Trap Defusal'
