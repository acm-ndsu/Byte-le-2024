from game.utils.vector import Vector
from game.common.items.item import Item


class AncientTech(Item):
    """
    Class for generic Ancient Tech item
    """
    def __init__(self, science_point_value: int = 1, quantity: int = 1, stack_size: int = 1, durability: int | None = None, position: Vector | None = None, name: str | None = None):
        super().__init__(0, science_point_value, quantity, stack_size, durability, position, name)
