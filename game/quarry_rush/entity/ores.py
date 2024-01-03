from game.utils.vector import Vector
from game.common.items.item import Item
from game.common.enums import *


class Ore(Item):
    """
    Class for generic Ore item.
    """
    def __init__(self, value: int = 1, quantity: int = 1, stack_size: int = 1, durability: int | None = None,
                 position: Vector | None = None, name: str | None = None):
        super().__init__(value, 0, quantity, stack_size, durability, position, name)
        self.object_type = ObjectType.ORE


class Lambdium(Ore):
    """
    Class representation of the Lambdium ore.
    """
    def __init__(self, value: int = 80, quantity: int = 1, stack_size: int = 1, durability: int | None = None,
                 position: Vector | None = None):
        super().__init__(value, 0, quantity, stack_size, durability, position)
        self.object_type = ObjectType.LAMBDIUM


class Turite(Ore):
    """
    Class representation of the Turite ore.
    """
    def __init__(self, value: int = 80, quantity: int = 1, stack_size: int = 1, durability: int | None = None,
                 position: Vector | None = None):
        super().__init__(value, 0, quantity, stack_size, durability, position)
        self.object_type = ObjectType.TURITE


class Copium(Ore):
    """
    Class representation of the Copium ore.
    """
    def __init__(self, value: int = 20, quantity: int = 1, stack_size: int = 1, durability: int | None = None,
                 position: Vector | None = None):
        super().__init__(value, 0, quantity, stack_size, durability, position)
        self.object_type = ObjectType.COPIUM
