import random

from game.common.enums import Company, ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from game.quarry_rush.entity.ores import Lambdium, Turite

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
        inventory: list[Item | None] = self.__inventories[company]
        def value(item: Item | None) -> int:
            return 0 if item is None else item.science_point_value
        return sum(map(value, inventory))

    def cash_in_points(self, company: Company) -> int:
        """
        Cashes in the points of every item in the appropriate inventory. Returns 0 if the given enum is incorrect.
        """
        inventory: list[Item | None] = self.__inventories[company]
        def value(item: Item | None) -> int:
            if item is None:
                return 0
            devaluation = 0.3
            if isinstance(item, Lambdium):
                return item.value if company == Company.CHURCH else round(item.value * devaluation)
            if isinstance(item, Turite):
                return item.value if company == Company.TURING else round(item.value * devaluation)
            return item.value
        return sum(map(value, inventory))

    def cash_in_all(self, company: Company) -> tuple[int, int]:
        """
        Runs both cash in methods: cash_in_science, cash_in_points.
        Removes all items from the appropriate inventory.
        """
        points = self.cash_in_points(company)
        science = self.cash_in_science(company)
        self.__inventories[company] = self.create_empty_inventory()
        return (points, science)

    def give(self, item: Item | None, company: Company) -> bool:
        """
        Give the selected player the given item. If the item was successfully given to the player, return True,
        otherwise False.
        """

        if item is None:
            return False

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

    def is_empty(self, company: Company) -> bool:
        """
        Returns True if first index is None, returns False otherwise
        """
        if self.__inventories[company][0] is None:
            return True
        else:
            return False

    def maybe_item_json(self, item: Item | None) -> dict | None:
        if item is None:
            return None
        return item.to_json()
    
    def inventories_json(self) -> dict:
        result: dict = {}
        for key in self.__inventories:
            result[key.value] = list(map(self.maybe_item_json, self.__inventories[key]))
        return result
            
    def maybe_item_from_json(self, item: dict | None) -> Item | None:
        if item is None:
            return None
        return Item().from_json(item)
            
    def from_inventories_json(self, data: dict) -> dict:
        result: dict = {}
        for key in data.keys():
            result[Company(int(key))] = list(map(self.maybe_item_from_json, data[key]))
        return result

    def to_json(self):
        data: dict = super().to_json()
        data['inventories'] = self.inventories_json()
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__inventories: dict[Company, list[Item | None]] = self.from_inventories_json(data['inventories'])
        return self
