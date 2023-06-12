from builtins import hasattr
from common.enums import Company

from game.common.items.item import Item


class InventoryManager(object):
    """
    This class is used to manage Avatar inventories.
    """
    
    __inventory_size = 50

    def __new__(cls):
        # This method only creates one singleton object of this class
        if not hasattr(cls, 'instance'):
            cls.instance = super(InventoryManager, cls).__new__(cls)
            cls.__inventories: dict[Company, list[Item | None]] = {
                Company.CHURCH: cls.create_empty_inventory(),
                Company.TURING: cls.create_empty_inventory()
            } 

            return cls.instance
        
    def create_empty_inventory(cls) -> list[Item | None]:
        new_inventory = []
        for i in range(0, cls.__inventory_size):
            new_inventory[i] = None
        return new_inventory

    def cash_in_science(self, company: Company) -> int:
        # Returns false instead of crashing if the given string doesn't exist in the dictionary.
        inventory = self.__inventories[company]

        total: int = 0

        for i in range(0, len(inventory)):
            if inventory[i] is not None:
                total += inventory[i].science_point_value
                inventory[i] = None

        return total

    def cash_in_gold(self, company: Company) -> int:
        # Returns false instead of crashing if the given string doesn't exist in the dictionary.
        inventory = self.__inventories[company]

        total: int = 0

        for i in range(0, len(inventory)):
            if inventory[i] is not None:
                total += inventory[i].value
                inventory[i] = None

        return total

    def give(self, item: Item, company: Company) -> bool:
        '''
        Give the selected player the given item. If the item was successfully given to the player, return True, otherwise False.
        '''
        inventory = self.__inventories[company]
        
        for i in range(0, len(inventory)):
            if inventory[i] is None:
                inventory[i] = item
                return True
        return False
