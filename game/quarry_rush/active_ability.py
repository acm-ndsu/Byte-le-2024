from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self
from game.common.avatar import Avatar


class ActiveAbility(GameObject):

    def __init__(self, name: str = "", avatar: Avatar | None = None, cooldown: int = 1, cooldown_tick: int = 0):
        super().__init__()
        self.object_type = ObjectType.ACTIVE_ABILITY
        self.name = name
        self.cooldown = cooldown
        self.cooldown_tick = cooldown_tick
        self.avatar: Avatar | None = avatar

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
    def avatar(self, avatar: Avatar) -> None:
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

# is_useable will be a boolean checking to see if the object on cooldown is able to be used again
    def is_useable(self) -> bool:
        return self.cooldown_tick == 0

# decrease cooldown, decrement cooldown: at the end of each turn it will have to be called for each avatar
    def decrease_cooldown_tick(self):
        self.__cooldown_tick -= 1  # calling the getter specifically
        if self.cooldown_tick < 0:
            self.cooldown_tick = 0  # so it cannot be negative

# reset cooldown tick: resetting the cooldown tick
    def reset_cooldown_tick(self):
        self.cooldown_tick = self.cooldown

# to json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['name'] = self.name
        data['cooldown'] = self.cooldown
        data['cooldown_tick'] = self.cooldown_tick
        data['avatar'] = self.avatar
        return data

# from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.name = data['name']
        self.cooldown = data['cooldown']
        self.cooldown_tick = data['cooldown_tick']
        self.avatar = data['avatar']
        return self







