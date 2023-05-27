from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.utils.vector import Vector
from game.common.items.item import Item
from typing import Self


class Ore(Item):
    def __init__(self, point_value: int = 1, value: int = 1, durability: int | None = None, quantity: int = 1, stack_size: int = 1, position: Vector | None = None, name: str | None = None):
        super.__init__(value,durability,quantity,stack_size,position,name)
        self.point_value: int = point_value 

    @property
    def point_value(self) -> int:
        return self.point_value
    


    @point_value.setter
    def point_value(self, point_value: int) -> None:
        if point_value is None or not isinstance(point_value, int):
            raise ValueError(f'{self.__class__.__name__}.point_value must be an int.')
        self.__value: int = point_value


    def to_json(self) -> dict:
        data: dict = super().to_json()
        
        data['point_value'] = self.point_value
        
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        
        self.point_value: int = data['point_value']
       
        return self
