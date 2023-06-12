from builtins import hasattr

from game.common.items.item import Item


class InventoryManager(object):
    """
    This class is used to manage Avatar inventories.
    """

    def __new__(cls):
        # This method only creates one singleton object of this class
        if not hasattr(cls, 'instance'):
            cls.instance = super(InventoryManager, cls).__new__(cls)
            cls.__inventories: dict[str, list[Item | None]] = {
                'church': [],
                'turing': []
            }  # Might change avatar_1 and avatar_2 to be the name of the company the avatar is working for in the lore

            return cls.instance

    def cash_in_science(self, player: str) -> int:
        # Returns false instead of crashing if the given string doesn't exist in the dictionary.
        if player not in self.__inventories.keys():
            return 0
        inventory = self.__inventories[player]

        total: int = 0

        for i in range(0, len(inventory)):
            if inventory[i] is not None:
                total += inventory[i].science_point_value
                inventory[i] = None

        return total

    def cash_in_gold(self, player: str) -> int:
        # Returns false instead of crashing if the given string doesn't exist in the dictionary.
        if player not in self.__inventories.keys():
            return 0
        inventory = self.__inventories[player]

        total: int = 0

        for i in range(0, len(inventory)):
            if inventory[i] is not None:
                total += inventory[i].value
                inventory[i] = None

        return total

    def give(self, item: Item, player: str) -> bool:
        pass
