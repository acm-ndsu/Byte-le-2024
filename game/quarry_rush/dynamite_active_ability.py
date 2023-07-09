from game.common.enums import ObjectType
from game.quarry_rush.active_ability import ActiveAbility
from game.utils.vector import Vector
from typing import Self


class DynamiteActiveAbility(ActiveAbility):

    def __init__(self,  position: Vector | None = None, name: str = ""):
        super().__init__()
        self.object_type = ObjectType.DYNAMITE_ACTIVE_ABILITY
        self.position: Vector = position
        self.name = name
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

# position getter
    @property
    def position(self) -> Vector | None:
        return self.__position

# position setter
    @position.setter
    def position(self, position: Vector | None) -> None:
        if position is not None and not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector or None.')
        self.__position = position

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
#     def place_dynamite(self):
        # ex of how i think it will be used:
        # player walks up to a specific location,
            # calls place dynamite to place the dynamite
            # wherever that player called place dynamite it will place the dynamite at that position
    # in this case, when the place dynamite is called
        # step 1: we need to get the current position of the player

# to json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['object_type'] = self.object_type
        data['position'] = self.position.to_json() if self.position is not None else None
        data['name'] = self.name
        data['cooldown'] = self.cooldown
        data['cooldown_tick'] = self.cooldown_tick
        return data

# from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.object_type = data['object_type']
        self.position = data['position']
        self.name = data['name']
        self.cooldown = data['cooldown']
        self.cooldown_tick = data['cooldown_tick']
        return self

