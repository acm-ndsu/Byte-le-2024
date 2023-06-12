import random

from game.common.enums import Company, ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item

from typing import Self


class InventoryManager(GameObject):
    """
    This class is used to manage Avatar inventories instead of the avatar instances doing so. This will only be
    created once in the project's lifespan, but is not enforced to be a singleton object.
    """

    __inventory_size: int = 50

    def __init__(self):
        super().__init__()
        self.object_type: ObjectType = ObjectType.INVENTORY_MANAGER
        self.__inventories: dict[Company, list[Item | None]] = {
            Company.CHURCH: self.create_empty_inventory(),
            Company.TURING: self.create_empty_inventory()
        }

    def create_empty_inventory(self) -> list[Item | None]:
        return [None] * self.__inventory_size

    def cash_in_science(self, company: Company) -> int:
        """
        Cashes in the science points of every item in the appropriate inventory. Returns 0 if the given enum is
        incorrect.
        """

        inventory = self.__inventories[company]

        total: int = 0

        for i in range(0, len(inventory)):
            if inventory[i] is not None:
                total += inventory[i].science_point_value
                inventory[i] = None

        return total

    def cash_in_gold(self, company: Company) -> int:
        """
        Cashes in the points of every item in the appropriate inventory. Returns 0 if the given enum is incorrect.
        """

        inventory = self.__inventories[company]

        total: int = 0

        for i in range(0, len(inventory)):
            if inventory[i] is not None:
                total += inventory[i].value
                inventory[i] = None

        return total

    def give(self, item: Item, company: Company) -> bool:
        """
        Give the selected player the given item. If the item was successfully given to the player, return True,
        otherwise False.
        """
        inventory = self.__inventories[company]

        for i in range(0, len(inventory)):
            if inventory[i] is None:
                inventory[i] = item
                return True
        return False

    def take(self, item: Item, company: Company) -> bool:
        """
        Takes the given item away from the given player. If the item was successfully take, return True, else False.
        """
        inventory = self.__inventories[company]

        for i in range(0, self.__inventory_size):
            if inventory[i].__eq__(item):
                inventory[i] = None
                return True
        return False

    def steal(self, to_company: Company, from_company: Company, steal_rate: float) -> None:
        """
        Take items from from_company and give them to to_company based on the steal_rate
        """
        from_inventory = self.__inventories[from_company]

        for item in list(filter(lambda i: i is not None, from_inventory)):
            if random.random() <= steal_rate:
                self.take(item, from_company)
                self.give(item, to_company)

    def get_inventory(self, company: Company) -> list[Item | None]:
        return self.__inventories[company]

    def to_json(self):
        data: dict = super().to_json()
        data['inventories'] = self.__inventories
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__inventories: dict[Company, list[Item | None]] = data['inventories']
        return self
