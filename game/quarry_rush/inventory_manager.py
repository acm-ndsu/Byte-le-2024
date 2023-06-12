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
        pass
    
    def cash_in_gold(self, player: str) -> int:
        pass

    def give(self, item: Item, player: str) -> bool:
        pass