from typing import Callable
from game.quarry_rush.avatar.avatar_functions import AvatarFunctions
from game.config import IMPROVED_DRIVETRAIN_COST, SUPERIOR_DRIVETRAIN_COST, OVERDRIVE_DRIVETRAIN_COST, LANDMINE_COST, \
    EMP_COST, IMPROVED_MINING_COST, SUPERIOR_MINING_COST, OVERDRIVE_MINING_COST, DYNAMITE_COST, TRAP_DEFUSAL_COST, \
    IMPROVED_DRIVETRAIN_POINTS, SUPERIOR_DRIVETRAIN_POINTS, OVERDRIVE_DRIVETRAIN_POINTS, IMPROVED_MINING_POINTS, \
    SUPERIOR_MINING_POINTS, OVERDRIVE_MINING_POINTS, DYNAMITE_POINTS, LANDMINE_POINTS, EMP_POINTS, TRAP_DEFUSAL_POINTS


class Tech:
    """
    This class represents a single tech. It contains the name, cost, point value, and effect
    of researching the tech
    """

    def __init__(self, name: str, cost: int, point_value: int, apply: Callable[[], None]):
        self.name = name
        self.cost = cost
        self.point_value = point_value
        self.apply = apply


class TechInfo:
    """
    This class contains information about a tech. It is basically Tech without the effect
    of researching the tech
    """

    def __init__(self, name: str, cost: int, point_value: int):
        self.name = name
        self.cost = cost
        self.point_value = point_value


def techs(avatar_functions: AvatarFunctions) -> dict[str, Tech]:
    """
    Creates the techs for a specific player
    """
    return {
        'Mining Robotics': Tech(
            name='Mining Robotics',
            cost=0,
            point_value=0,
            apply=lambda: None
        ),

        'Improved Drivetrain': Tech(
            name='Improved Drivetrain',
            cost=IMPROVED_DRIVETRAIN_COST,
            point_value=IMPROVED_DRIVETRAIN_POINTS,
            apply=lambda: avatar_functions.increase_movement(1)
        ),

        'Improved Mining': Tech(
            name='Improved Mining',
            cost=IMPROVED_MINING_COST,
            point_value=IMPROVED_MINING_POINTS,
            apply=lambda: avatar_functions.increase_mining(1)
        ),

        'Dynamite': Tech(
            name='Dynamite',
            cost=DYNAMITE_COST,
            point_value=DYNAMITE_POINTS,
            apply=avatar_functions.unlock_dynamite
        ),

        'Superior Drivetrain': Tech(
            name='Superior Drivetrain',
            cost=SUPERIOR_DRIVETRAIN_COST,
            point_value=SUPERIOR_DRIVETRAIN_POINTS,
            apply=lambda: avatar_functions.increase_movement(1)
        ),

        'Superior Mining': Tech(
            name='Superior Mining',
            cost=SUPERIOR_MINING_COST,
            point_value=SUPERIOR_MINING_POINTS,
            apply=lambda: avatar_functions.increase_mining(1)
        ),

        'Landmines': Tech(
            name='Landmines',
            cost=LANDMINE_COST,
            point_value=LANDMINE_POINTS,
            apply=avatar_functions.unlock_landmines
        ),

        'Overdrive Drivetrain': Tech(
            name='Overdrive Drivetrain',
            cost=OVERDRIVE_DRIVETRAIN_COST,
            point_value=OVERDRIVE_DRIVETRAIN_POINTS,
            apply=avatar_functions.unlock_movement_overdrive
        ),

        'Overdrive Mining': Tech(
            name='Overdrive Mining',
            cost=OVERDRIVE_MINING_COST,
            point_value=OVERDRIVE_MINING_POINTS,
            apply=avatar_functions.unlock_mining_overdrive
        ),

        'EMPs': Tech(
            name='EMPs',
            cost=EMP_COST,
            point_value=EMP_POINTS,
            apply=avatar_functions.unlock_emps
        ),

        'Trap Defusal': Tech(
            name='Trap Defusal',
            cost=TRAP_DEFUSAL_COST,
            point_value=TRAP_DEFUSAL_POINTS,
            apply=avatar_functions.unlock_trap_defusal
        )
    }
