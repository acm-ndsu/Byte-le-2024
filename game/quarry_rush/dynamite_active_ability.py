from game.common.enums import ObjectType
from game.quarry_rush.active_ability import ActiveAbility
from typing import Self


class DynamiteActiveAbility(ActiveAbility):

    def __init__(self, cooldown: int = 1, fuse: int = 0):
        super().__init__()
        self.object_type = ObjectType.DYNAMITE_ACTIVE_ABILITY
        self.cooldown: int = 1
        self.fuse: int = 0
        self.placing_dynamite: bool = False  # this is a boolean check to see if the avatar is placing down dynamite

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
    def fuse(self) -> int:
        return self.__fuse

# cooldown tick setter
    @fuse.setter
    def fuse(self, fuse: int) -> None:
        if fuse is None or not isinstance(fuse, int):
            raise ValueError(f'{self.__class__.__name__}.fuse must be an int')
        if fuse < 0:
            raise ValueError(f'{self.__class__.__name__}.fuse cannot be negative')
        self.__fuse = fuse

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
        data['cooldown'] = self.cooldown
        data['fuse'] = self.fuse
        data['placing_dynamite'] = self.placing_dynamite
        return data

# from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.object_type = data['object_type']
        self.cooldown = data['cooldown']
        self.fuse = data['fuse']
        self.placing_dynamite = data['placing_dynamite']
        return self

