from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self
from game.quarry_rush.active_ability import ActiveAbility
from game.common.avatar import Avatar


class DynamiteActiveAbility(ActiveAbility):

    def __init__(self, name: str, avatar: Avatar | None = None):
        super().__init__()
        self.object_type = ObjectType.DYNAMITE_ACTIVE_ABILITY
        self.name = name
        self.avatar: Avatar | None = avatar
        self.cooldown: int = 1
        self.cooldown_tick: int = 0

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

# avatar getter
    @property
    def avatar(self) -> Avatar:
        return self.__avatar

# avatar setter
    @avatar.setter
    def avatar(self, avatar: Avatar | None) -> None:
        if avatar is not None and not isinstance(avatar, Avatar):
            raise ValueError(f'{self.__class__.__name__}.avatar must be Avatar or None')
        self.__avatar = avatar

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

# place dynamite

