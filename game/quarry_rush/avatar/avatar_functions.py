from typing import Callable


class AvatarFunctions:
    """
    This class is used as an interface for creating a tech tree

    Attributes
    ----------
    * increase_movement: A function that takes an int for the amount to
    increase movement speed by and increases the movement speed of the
    player

    * increase_mining: A function that takes a float for the amount to
    increase mining drop rate by and increases the mining drop rate of
    the player

    * unlock_movement_overdrive: A function that unlocks the movement
    overdrive ability for the player

    * unlock_mining_overdrive: A function that unlocks the mining overdrive
    ability for the player

    * unlock_dynamite: A function that unlocks dynamite for the player

    * unlock_landmines: A function that unlocks landmines for the player

    * unlock_emps: A function that unlocks emps for the player

    * unlock_trap_defusal: A function that unlocks trap defusal for the player
    """

    def __init__(self,
                 increase_movement: Callable[[int], None],
                 increase_mining: Callable[[int], None],
                 unlock_movement_overdrive: Callable[[], None],
                 unlock_mining_overdrive: Callable[[], None],
                 unlock_dynamite: Callable[[], None],
                 unlock_landmines: Callable[[], None],
                 unlock_emps: Callable[[], None],
                 unlock_trap_defusal: Callable[[], None]):
        self.increase_movement = increase_movement
        self.increase_mining = increase_mining
        self.unlock_movement_overdrive = unlock_movement_overdrive
        self.unlock_mining_overdrive = unlock_mining_overdrive
        self.unlock_dynamite = unlock_dynamite
        self.unlock_landmines = unlock_landmines
        self.unlock_emps = unlock_emps
        self.unlock_trap_defusal = unlock_trap_defusal
