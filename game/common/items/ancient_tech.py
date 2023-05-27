from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.utils.vector import Vector
from game.common.items.item import Item
from typing import Self


class Ancient_Tech(Item):
    def __init__(self, science_point_value: int = 1, value: int = 1, durability: int | None = None, quantity: int = 1, stack_size: int = 1, position: Vector | None = None, name: str | None = None):
        super.__init__(value,durability,quantity,stack_size,position,name)
        self.science_point_value: int = science_point_value 

    @property
    def science_point_value(self) -> int:
        return self.__science_point_value
    


    @science_point_value.setter
    def science_point_value(self, science_point_value: int) -> None:
        if science_point_value is None or not isinstance(science_point_value, int):
            raise ValueError(f'{self.__class__.__name__}.science_point_value must be an int.')
        self.__value: int = science_point_value


    def to_json(self) -> dict:
        data: dict = super().to_json()
        
        data['science_point_value'] = self.science_point_value
        
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        
        self.science_point_value: int = data['science_point_value']
       
        return self
