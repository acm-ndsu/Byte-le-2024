from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from game.utils.vector import Vector
from typing import Self


class Avatar(GameObject):
    """
    Notes for the inventory:

    The avatar's inventory is a list of items. Each item has a quantity and a stack_size (the max amount of an
    item that can be held in a stack. Think of the Minecraft inventory).

    This upcoming example is just to facilitate understanding the concept. The Dispensing Station concept that will
    be mentioned is completely optional to implement if you desire. The Dispensing Station is used to help with the
    explanation.

    ----------------------------------------------------------------------------------------------------------------

    Items:
        Every Item has a quantity and a stack_size. The quantity is how much of the Item the player *currently* has.
        The stack_size is the max of that Item that can be in a stack. For example, if the quantity is 5, and the
        stack_size is 5 (5/5), the item cannot be added to that stack

    Picking up items:
    Example 1:
        When you pick up an item (which will now be referred to as picked_up_item), picked_up_item has a given
        quantity. In this case, let's say the quantity of picked_up_item is 2.

        Imagine you already have this item in your inventory (which will now be referred to as inventory_item),
        and inventory_item has a quantity of 1 and a stack_size of 10 (think of this as a fraction: 1/10).

        When you pick up picked_up_item, inventory_item will be checked.
        If picked_up_item's quantity + inventory_item < stack_size, it'll be added without issue.
        Remember, for this example: picked_up_item quantity is 2, and inventory_item quantity is 1, and stack_size
        is 10.
            Inventory_item quantity before picking up: 1/10
                2 + 1 < 10 --> True
            Inventory_item quantity after picking up: 3/10

    ----------------------------------------------------------------------------------------------------------------

    Example 2:
        For the next two examples, the total inventory size will be considered.

        Let's say inventory_item has quantity 4 and a stack_size of 5. Now say that picked_up_item has quantity 3.
        Recall: if picked_up_item's quantity + inventory_item < stack_size, it will be added without issue
            Inventory_item quantity before picking up: 4/5
                3 + 4 < 5 --> False

        What do we do in this situation? If you want to add picked_up_item to inventory_item and there is an
        overflow of quantity, that is handled for you.

        Let's say that your inventory size (which will now be referred to as max_inventory_size) is 5. You already
        have inventory_item in there that has a quantity of 4 and a stack_size of 5. An image of the inventory is
        below. 'None' is used to help show the max_inventory_size. Inventory_item quantity and stack_size will be
        listed in parentheses as a fraction.
            Inventory:
            [inventory_item (4/5), None, None, None, None]

        Now we will add picked_up_item and its quantity of 3:
            Inventory before:
            [inventory_item (4/5), None, None, None, None]

            3 + 4 < 5 --> False
                inventory_item (4/5) will now be inventory_item (5/5)
                picked_up_item now has a quantity of 2
                Since we have a surplus, we will append the same item with a quantity of 2 in the inventory.

            The result is:
            [inventory_item (5/5), inventory_item (2/5), None, None, None]

    ----------------------------------------------------------------------------------------------------------------
    Example 3:

        For this last example, assume your inventory looks like this:
        [inventory_item (5/5), inventory_item (5/5) inventory_item (5/5) inventory_item (5/5), inventory_item (4/5)]

        You can only fit one more inventory_item into the last stack before the inventory is full.
        Let's say that picked_up_item has quantity of 3 again.

        Inventory before:
        [inventory_item (5/5), inventory_item (5/5) inventory_item (5/5) inventory_item (5/5), inventory_item (4/5)]
            3 + 4 < 5 --> False
            inventory_item (4/5) will now be inventory_item (5/5)
            picked_up_item now has a quantity of 2
            However, despite the surplus, we cannot add it into our inventory, so the remaining quantity of
            picked_up_item is left where it was first found.
        Inventory after:
        [inventory_item (5/5), inventory_item (5/5) inventory_item (5/5) inventory_item (5/5), inventory_item (5/5)]
    """

    def __init__(self, item: Item | None = None, position: Vector | None = None, inventory: list[Item] = [],
                 max_inventory_size: int = 10):
        super().__init__()
        self.object_type: ObjectType = ObjectType.AVATAR
        self.held_item: Item | None = item
        self.score: int = 0
        self.position: Vector | None = position
        self.max_inventory_size: int = max_inventory_size
        self.inventory: list[Item] = inventory

    @property
    def held_item(self) -> Item | None:
        return self.__held_item

    @property
    def score(self) -> int:
        return self.__score

    @property
    def position(self) -> Vector | None:
        return self.__position

    @property
    def inventory(self) -> list[Item]:
        return self.__inventory

    @property
    def max_inventory_size(self) -> int:
        return self.__max_inventory_size

    @held_item.setter
    def held_item(self, item: Item | None) -> None:
        # If it's not an item, and it's not None, raise the error
        if item is not None and not isinstance(item, Item):
            raise ValueError(f'{self.__class__.__name__}.held_item must be an Item or None.')
        self.__held_item: Item = item

    @score.setter
    def score(self, score: int) -> None:
        if score is None or not isinstance(score, int):
            raise ValueError(f'{self.__class__.__name__}.score must be an int.')
        self.__score: int = score

    @position.setter
    def position(self, position: Vector | None) -> None:
        if position is not None and not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector or None.')
        self.__position: Vector | None = position

    @inventory.setter
    def inventory(self, inventory: list[Item]) -> None:
        if inventory is None or not isinstance(inventory, list) \
                or (len(inventory) > 0 and any(map(lambda item: not isinstance(item, Item), inventory))):
            raise ValueError(f'{self.__class__.__name__}.inventory must be a list of Items.')
        if len(inventory) > self.max_inventory_size:
            raise ValueError(f'{self.__class__.__name__}.inventory size must be less than max_inventory_size')
        self.__inventory: list[Item] = inventory

    @max_inventory_size.setter
    def max_inventory_size(self, size: int) -> None:
        if size is None or not isinstance(size, int):
            raise ValueError(f'{self.__class__.__name__}.max_inventory_size must be an int.')
        self.__max_inventory_size: int = size

    def pick_up(self, item: Item) -> Item | None:
        t = item
        [t := i.pick_up(t) for i in self.inventory]

        if t is not None and len(self.inventory) < self.max_inventory_size:
            self.inventory.append(t)
            return None

        return t

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['held_item'] = self.held_item.to_json() if self.held_item is not None else None
        data['score'] = self.score
        data['position'] = self.position.to_json() if self.position is not None else None 
        data['inventory'] = self.inventory
        data['max_inventory_size'] = self.max_inventory_size
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.score: int = data['score']
        self.position: Vector | None = None if data['position'] is None else Vector().from_json(data['position'])
        self.inventory: list[Item] = data['inventory']
        self.max_inventory_size: int = data['max_inventory_size']
        held_item: Item | None = data['held_item']
        if held_item is None:
            self.held_item = None
            return self

        match held_item['object_type']:
            case ObjectType.ITEM:
                self.held_item = Item().from_json(data['held_item'])
            case _:
                raise ValueError(f'{self.__class__.__name__}.held_item needs to be an item.')

        return self
