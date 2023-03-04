from game.common.game_object import GameObject
from game.common.enums import ObjectType
from typing import Self

class Vector(GameObject):
    def __init__(self, x: int = 0, y: int = 0):
           super().__init__()
           self.object_type: ObjectType = ObjectType.VECTOR
           self.x = x
           self.y = y

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if x is None or not isinstance(x, int):
            raise ValueError(f"The given x value, {x}, is not an integer.")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, y: int):
        if y is None or not isinstance(y, int):
            raise ValueError(f"The given y value, {y}, is not an integer.")
        self.__y = y

    def to_json(self) -> dict:
        data = super().to_json()
        data['x'] = self.x
        data['y'] = self.y

        return data

    def from_json(self, data) -> Self:
        super().from_json(data)
        self.x = data['x']
        self.y = data['y']

        return self

    def __str__(self) -> str:
        return f"Coordinates: ({self.x}, {self.y})"