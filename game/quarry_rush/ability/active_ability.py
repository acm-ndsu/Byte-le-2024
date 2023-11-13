from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self


class ActiveAbility(GameObject):

    def __init__(self, cooldown: int = 1, fuse: int = 0):
        super().__init__()
        self.object_type = ObjectType.ACTIVE_ABILITY
        self.cooldown = cooldown
        self.fuse = fuse

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

# fuse is the time it takes before the ability is able to be used again
# fuse getter
    @property
    def fuse(self) -> int:
        return self.__fuse

# fuse setter
    @fuse.setter
    def fuse(self, fuse: int) -> None:
        if fuse is None or not isinstance(fuse, int):
            raise ValueError(f'{self.__class__.__name__}.fuse must be an int')
        if fuse < 0:
            raise ValueError(f'{self.__class__.__name__}.fuse cannot be negative')
        self.__fuse = fuse

# use will be a boolean checking to see if the object on cooldown is able to be used again
    def is_useable(self) -> bool:
        if self.fuse == 0:
            return True
        return False

# decrease cooldown, decrement cooldown: at the end of each turn it will have to be called for each avatar
    def decrease_fuse(self):
        self.__fuse -= 1  # calling the getter specifically
        if self.fuse < 0:
            self.fuse = 0  # so it cannot be negative

# reset cooldown tick: resetting the cooldown tick
    def reset_fuse(self):
        self.fuse = self.cooldown

# to json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['cooldown'] = self.cooldown
        data['fuse'] = self.fuse
        return data

# from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.cooldown = data['cooldown']
        self.fuse = data['fuse']
        return self
