from typing import Callable
from game.quarry_rush.avatar.avatar_functions import AvatarFunctions


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
            cost=50,
            point_value=200,
            apply=lambda: avatar_functions.increase_movement(1)
        ),

        'Improved Mining': Tech(
            name='Improved Mining',
            cost=50,
            point_value=100,
            apply=lambda: avatar_functions.increase_mining(1)
        ),

        'Dynamite': Tech(
            name='Dynamite',
            cost=150,
            point_value=500,
            apply=avatar_functions.unlock_dynamite
        ),

        'Superior Drivetrain': Tech(
            name='Superior Drivetrain',
            cost=100,
            point_value=400,
            apply=lambda: avatar_functions.increase_movement(1)
        ),

        'Superior Mining': Tech(
            name='Superior Mining',
            cost=100,
            point_value=200,
            apply=lambda: avatar_functions.increase_mining(1)
        ),

        'Landmines': Tech(
            name='Landmines',
            cost=300,
            point_value=1000,
            apply=avatar_functions.unlock_landmines
        ),

        'Overdrive Drivetrain': Tech(
            name='Overdrive Drivetrain',
            cost=250,
            point_value=1600,
            apply=avatar_functions.unlock_movement_overdrive
        ),

        'Overdrive Mining': Tech(
            name='Overdrive Mining',
            cost=250,
            point_value=800,
            apply=avatar_functions.unlock_mining_overdrive
        ),

        'EMPs': Tech(
            name='EMPs',
            cost=450,
            point_value=2000,
            apply=avatar_functions.unlock_emps
        ),

        'Trap Defusal': Tech(
            name='Trap Defusal',
            cost=450,
            point_value=2000,
            apply=avatar_functions.unlock_trap_defusal
        )
    }
