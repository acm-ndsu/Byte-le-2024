from typing import Callable
from game.quarry_rush.player_functions import PlayerFunctions

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
        
def techs(player_functions: PlayerFunctions) -> dict[str, Tech]:
    """
    Creates the techs for a specific player
    """
    def combine(*things: Callable[[], None]) -> None:
        for thing in things:
            thing()

    return {
        'Mining Robotics': Tech(
            name='Mining Robotics',
            cost=0,
            point_value=0,
            apply=lambda : None
        ),
        
        'Better Drivetrains': Tech(
            name='Better Drivetrains',
            cost=0,
            point_value=1,
            apply=lambda : player_functions.increase_movement(1)
        ),
        
        'High Yield Drilling': Tech(
            name='High Yield Drilling',
            cost=0,
            point_value=1,
            apply=lambda : player_functions.increase_mining(0.2)
        ),
        
        'Dynamite': Tech(
            name='Dynamite',
            cost=0,
            point_value=1,
            apply=player_functions.unlock_dynamite
        ),
        
        'Unnamed Drivetrain Tech': Tech(
            name='Unnamed Drivetrain Tech',
            cost=0,
            point_value=1,
            apply=lambda : player_functions.increase_movement(1)
        ),
        
        'Unnamed Mining Tech': Tech(
            name='Unnamed Mining Tech',
            cost=0,
            point_value=1,
            apply=lambda : player_functions.increase_mining(0.2)
        ),
        
        'Landmines': Tech(
            name='Landmines',
            cost=0,
            point_value=1,
            apply=lambda : combine(player_functions.unlock_landmines, lambda : player_functions.increase_stealing(0.2))
        ),
        
        'Overdrive Movement': Tech(
            name='Overdrive Movement',
            cost=0,
            point_value=1,
            apply=player_functions.unlock_movement_overdrive
        ),
        
        'Overdrive Mining': Tech(
            name='Overdrive Mining',
            cost=0,
            point_value=1,
            apply=player_functions.unlock_mining_overdrive
        ),
        
        'EMPs': Tech(
            name='EMPs',
            cost=0,
            point_value=1,
            apply=lambda : combine(player_functions.unlock_emps, lambda : player_functions.increase_stealing(0.2))
        ),
        
        'Trap Detection': Tech(
            name='Trap Detection',
            cost=0,
            point_value=1,
            apply=player_functions.unlock_trap_detection
        )
    }