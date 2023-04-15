from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self


class Item(GameObject):
    def __init__(self, value: int = 1, durability: int | None = 100, quantity: int = 1, stack_size: int = 1):
        super().__init__()
        self.__quantity = None  # This is here to prevent an error
        self.object_type: ObjectType = ObjectType.ITEM
        self.value: int = value  # Value can more specified based on purpose (e.g., the sell price)
        self.stack_size: int = stack_size  # the max quantity this item can contain
        self.durability: int | None = durability  # durability can be None if infinite durability
        self.quantity: int = quantity  # the current amount of this item

    @property
    def durability(self) -> int | None:
        return self.__durability

    @property
    def value(self) -> int:
        return self.__value

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def stack_size(self) -> int:
        return self.__stack_size

    @durability.setter
    def durability(self, durability: int | None):
        if durability is not None and not isinstance(durability, int) or self.stack_size > 1:
            raise ValueError(f'{self.__class__.__name__}.durability must be an int or None, and stack_size must be 1.')
        self.__durability = durability

    @value.setter
    def value(self, value: int) -> None:
        if value is None or not isinstance(value, int):
            raise ValueError(f'{self.__class__.__name__}.value must be an int.')
        self.__value: int = value

    @quantity.setter
    def quantity(self, quantity: int) -> None:
        if quantity is None or not isinstance(quantity, int):
            raise ValueError(f'{self.__class__.__name__}.quantity must be an int.')
        if quantity < 0:
            raise ValueError(f'{self.__class__.__name__}.quantity must be greater than 0.')

        # The self.quantity is set to the lower value between stack_size and the given quantity
        # The remaining given quantity is returned if it's larger than self.quantity
        if quantity > self.stack_size:
            raise ValueError(f'{self.__class__.__name__}.quantity cannot be greater than '
                             f'{self.__class__.__name__}.stack_size')
        self.__quantity: int = quantity

    @stack_size.setter
    def stack_size(self, stack_size: int) -> None:
        if stack_size is None or not isinstance(stack_size, int):
            raise ValueError(f'{self.__class__.__name__}.stack_size must be an int.')
        if self.__quantity is not None and stack_size < self.__quantity:
            raise ValueError(f'{self.__class__.__name__}.stack_size must be greater than or equal to the quantity.')
        self.__stack_size: int = stack_size

    def pick_up(self, item: Self) -> Self | None:
        # If the items don't match, return the given item without modifications
        if self.object_type != item.object_type:
            return item

        # If the picked up quantity goes over the stack_size, add to make the quantity equal the stack_size
        if self.quantity + item.quantity > self.stack_size:
            item.quantity -= self.stack_size - self.quantity
            self.quantity: int = self.stack_size
            return item

        # Add the given item's quantity to the self item
        self.quantity += item.quantity

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['durability'] = self.durability
        data['value'] = self.value
        data['quantity'] = self.quantity
        data['stack_size'] = self.stack_size
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.durability: int | None = data['durability']
        self.value: int = data['value']
        self.quantity: int = data['quantity']
        self.stack_size: int = data['stack_size']
        return self
