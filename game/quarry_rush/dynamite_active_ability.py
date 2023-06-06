from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self
from game.quarry_rush.active_ability import ActiveAbility

class DynamiteActiveAbility(ActiveAbility):

    def __init__(self, name: str, cooldown: int, cooldown_tick: int):
        super().__init__()
        self.object_type = ObjectType.DYNAMITE_ACTIVE_ABILITY
        self.name = name
        self.cooldown = cooldown
        self.cooldown_tick = cooldown_tick

# name getter
    @property
    def name(self) -> str:
        return self.__name

# name setter
    @name.setter
    def name(self, name: str) -> None:
        if name is None or not isinstance(name, str):
            raise ValueError(f'{self.__class__.__name__}.name must be a String')
        self.__name = name

# The cooldown represents the amount of turns that the ability is unavailable.
# cooldown getter
    @property
    def cooldown(self) -> int:
        return self.__cooldown

# cooldown setter
    @cooldown.setter
    def cooldown(self, cooldown: int) -> None:
        if cooldown is None or not isinstance(cooldown, int):
            raise ValueError(f'{self.__class__.__name__}.cooldown must be an int')
        if cooldown < 0:
            raise ValueError(f'{self.__class__.__name__}.cooldown cannot be negative')
        self.__cooldown = cooldown

# cooldown tick is the time it takes before the ability is able to be used again
# cooldown tick getter
    @property
    def cooldown_tick(self) -> int:
        return self.__cooldown_tick

# cooldown tick setter
    @cooldown_tick.setter
    def cooldown_tick(self, cooldown_tick: int) -> None:
        if cooldown_tick is None or not isinstance(cooldown_tick, int):
            raise ValueError(f'{self.__class__.__name__}.cooldown_tick must be an int')
        if cooldown_tick < 0:
            raise ValueError(f'{self.__class__.__name__}.cooldown_tick cannot be negative')
        self.__cooldown_tick = cooldown_tick

# unlock from tech tree

# place dynamite

