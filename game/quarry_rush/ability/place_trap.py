from game.quarry_rush.ability.active_ability import ActiveAbility
from game.common.enums import ObjectType
from typing import Self


class PlaceTrap(ActiveAbility):

    def __init__(self, cooldown: int = 1, cooldown_tick: int = 0):
        super().__init__()
        self.object_type: ObjectType = ObjectType.PLACE_TRAP
        self.cooldown: int = cooldown
        self.cooldown_tick: int = cooldown_tick
        self.placing_trap: bool = False

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

    # placing dynamite getter
    @property
    def placing_trap(self) -> bool:
        return self.__placing_trap

    # placing dynamite setter
    @placing_trap.setter
    def placing_trap(self, placing_trap: bool):
        if placing_trap is None or not isinstance(placing_trap, bool):
            raise ValueError(f'{self.__class__.__name__}.placing_trap must be a bool.')
        self.__placing_trap = placing_trap

    # to json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['cooldown'] = self.cooldown
        data['cooldown_tick'] = self.cooldown_tick
        data['placing_trap'] = self.placing_trap
        return data

    # from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.cooldown = data['cooldown']
        self.cooldown_tick = data['cooldown_tick']
        self.placing_trap = data['placing_trap']
        return self
