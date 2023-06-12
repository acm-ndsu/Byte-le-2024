from game.common.enums import Company

from game.common.items.item import Item


class InventoryManager(object):
    """
    This class is used to manage Avatar inventories instead of the avatar instances doing so. This will only be
    created once in the project's lifespan, but is not enforced to be a singleton object.
    """

    __inventory_size: int = 50

    def __init__(self):
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
