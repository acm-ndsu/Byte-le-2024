from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.utils.vector import Vector
from typing import Self
from game.common.items.item import Item

class DynamiteItem(Item):
    def __init__(self, value: int = 1, durability: int | None = None, quantity: int = 1, stack_size: int = 1,
                 position: Vector | None = None, name: str | None = None):
        self.value: int | None= None
        self.durability: int | None = None
        self.quantity: int = 1
