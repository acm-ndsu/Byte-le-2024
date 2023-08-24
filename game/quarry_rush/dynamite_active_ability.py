from game.common.enums import ObjectType
from game.quarry_rush.active_ability import ActiveAbility
from typing import Self


class DynamiteActiveAbility(ActiveAbility):

    def __init__(self, name: str = ""):
        super().__init__()
        self.object_type = ObjectType.DYNAMITE_ACTIVE_ABILITY
        self.name = name
        self.cooldown: int = 1
        self.cooldown_tick: int = 0
        self.placing_dynamite: bool = False  # this is a boolean check to see if the avatar is placing down dynamite

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

# placing dynamite getter
    @property
    def placing_dynamite(self) -> bool:
        return self.__placing_dynamite

# placing dynamite setter
    @placing_dynamite.setter
    def placing_dynamite(self, placing_dynamite: bool):
        if placing_dynamite is None or not isinstance(placing_dynamite, bool):
            raise ValueError(f'{self.__class__.__name__}.placing_dynamite must be a bool.')
        self.__placing_dynamite = placing_dynamite

# to json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['object_type'] = self.object_type
        data['name'] = self.name
        data['cooldown'] = self.cooldown
        data['cooldown_tick'] = self.cooldown_tick
        data['placing_dynamite'] = self.placing_dynamite
        return data

# from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.object_type = data['object_type']
        self.name = data['name']
        self.cooldown = data['cooldown']
        self.cooldown_tick = data['cooldown_tick']
        self.placing_dynamite = data['placing_dynamite']
        return self

