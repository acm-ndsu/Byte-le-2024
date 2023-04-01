from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.utils.vector import Vector
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

    @staticmethod
    def add_vectors(vector_1: Vector, vector_2: Vector) -> Vector:
        new_x: int = vector_1.x + vector_2.x
        new_y: int = vector_1.y + vector_2.y
        return Vector(new_x, new_y)

    def add_to_vector(self, other_vector: Vector):
        self.x += other_vector.x
        self.y += other_vector.y

    def add_x_y(self, x: int, y: int):
        self.x += x
        self.y += y

    def add_x(self, x: int):
        self.x += x

    def add_y(self, y: int):
        self.y += y

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
