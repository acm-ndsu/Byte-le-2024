from game.quarry_rush.ability.active_ability import ActiveAbility
from game.common.enums import ObjectType
from typing import Self


class PlaceTrap(ActiveAbility):

    def __init__(self, cooldown: int = 1, fuse: int = 0):
        super().__init__()
        self.object_type: ObjectType = ObjectType.PLACE_TRAP
        self.cooldown: int = cooldown
        self.fuse: int = fuse
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
    def fuse(self) -> int:
        return self.__fuse

    # setter for cooldown tick
    @fuse.setter
    def fuse(self, fuse: int) -> None:
        if fuse is None or not isinstance(fuse, int):
            raise ValueError(f'{self.__class__.__name__}.fuse must be an int')
        self.__fuse = fuse

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
        data['fuse'] = self.fuse
        data['placing_trap'] = self.placing_trap
        return data

    # from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.cooldown = data['cooldown']
        self.fuse = data['fuse']
        self.placing_trap = data['placing_trap']
        return self
