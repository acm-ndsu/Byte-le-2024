from game.quarry_rush.active_ability import ActiveAbility
from game.common.avatar import Avatar


class PlaceTrap(ActiveAbility):

    def __init__(self, name: str = "", cooldown: int = 1, cooldown_tick: int = 0, avatar: Avatar | None = None):
        super().__init__()
        self.name: str = name
        self.cooldown: int = cooldown
        self.cooldown_tick: int = cooldown_tick
        self.avatar: Avatar | None = avatar

    # getter for name
    @property
    def name(self) -> str:
        return self.__name

    # setter for name
    @name.setter
    def name(self, name: str) -> None:
        if name is None or not isinstance(name, str):
            raise ValueError(f'{self.__class__.__name__}.name must be a String')
        self.__name = name

    # getter for cooldown
    @property
    def cooldown(self) -> int:
        return self.__cooldown

    # setter for cooldown
    @cooldown.setter
    def cooldown(self, cooldown: int) -> None:
        if cooldown is None or not isinstance(cooldown, int):
            raise ValueError(f'{self.__class__.__name__}.cooldown must be an int')
        self.__cooldown = cooldown

    # getter for cooldown tick
    @property
    def cooldown_tick(self) -> int:
        return self.__cooldown_tick

    # setter for cooldown tick
    @cooldown_tick.setter
    def cooldown_tick(self, cooldown_tick: int) -> None:
        if cooldown_tick is None or not isinstance(cooldown_tick, int):
            raise ValueError(f'{self.__class__.__name__}.cooldown_tick must be an int')
        self.__cooldown_tick = cooldown_tick

    # getter for avatar
    @property
    def avatar(self) -> Avatar:
        return self.__avatar

    # setter for avatar
    @avatar.setter
    def avatar(self, avatar: Avatar) -> None:
        if avatar is not None and not isinstance(avatar, Avatar):
            raise ValueError(f'{self.__class__.__name__}.avatar must be Avatar or None')
        self.__avatar = avatar

# method for place trap

# cooldown decrease?

# cooldown reset?

# is use-able?



