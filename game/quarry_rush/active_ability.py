from game.common.enums import ObjectType
from game.common.game_object import GameObject


class ActiveAbility(GameObject):

    def __init__(self, name: str = "temp", cooldown: int = 1):
        super().__init__()
        self.object_type = ObjectType
        self.name: str = name
        self.cooldown: int = cooldown

# name getter
    @property
    def name(self) -> str:
        return self.__name

# name setter
    @name.setter
    def name(self, name: str):
        if name is not isinstance(name, str):
            raise ValueError(f'{self.__class__.__name__}.name must be a String')
        self.__name = name

# The cooldown represents the amount of turns that the ability is unavailable.
# cooldown getter
    @property
    def cooldown(self) -> int:
        return self.__cooldown

# cooldown setter
    @cooldown.setter
    def cooldown(self, cooldown: int) -> 1:   # currently I just have the default set to 1, should not be negative
        if cooldown is not isinstance(cooldown, int):
            raise ValueError(f'{self.__class__.__name__}.cooldown must be an int')
        self.__cooldown = cooldown

    # to json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['name'] = self.name
        data['cooldown'] = self.cooldown
        return data

    # from json
    def from_json(self, data: dict):
        super().from_json(data)
        self.name: str = data['name']
        self.cooldown: int = data['cooldown']
        return self






