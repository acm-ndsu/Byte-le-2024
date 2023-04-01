from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self


class Item(GameObject):
    def __init__(self, value: int = 1, durability: int | None = 100):
        super().__init__()
        self.object_type: ObjectType = ObjectType.ITEM
        self.value: int = value
        self.durability: int | None = durability # durability can be None if infinite durability
        
    @property
    def durability(self) -> int | None:
        return self.__durability

    @property
    def value(self) -> int:
        return self.__value

    @durability.setter
    def durability(self, durability: int | None) -> None:
        if durability is not None and not isinstance(durability, int):
            raise ValueError(f'{self.__class__.__name__}.durability must be an int or None.')
        self.__durability = durability

    @value.setter
    def value(self, value: int) -> None:
        if value is None or not isinstance(value, int):
            raise ValueError(f'{self.__class__.__name__}.value must be an int.')
        self.__value = value

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['durability'] = self.durability
        data['value'] = self.value
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.durability: int | None = data['durability']
        self.value: int = data['value']
        return self
