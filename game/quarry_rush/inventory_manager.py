from builtins import hasattr

from game.common.avatar import Avatar
from game.common.items.item import Item
from typing import Self

class InventoryManager(object):
    """
    This class is used to manage Avatar inventories.
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(InventoryManager, cls).__new__(cls)
            return cls.instance

    def __clean_inventory(self) -> None:
        """
        This method is used to manage the inventory. Whenever an item has a quantity of 0, it will set that item object
            to None since it doesn't exist in the inventory anymore. Otherwise, if there are multiple instances of an
            item in the inventory, and they can be consolidated, this method does that.

        Example: In inventory[0], there is a stack of gold with a quantity and stack_size of 5. In inventory[1], there
            is another stack of gold with quantity of 3, stack size of 5. If you want to take away 4 gold, inventory[0]
            will have quantity 1, and inventory[1] will have quantity 3. Then, when clean_inventory is called, it will
            consolidate the two. This mean that inventory[0] will have quantity 4 and inventory[1] will be set to None.
        :return: None
        """

        # This condenses the inventory if there are duplicate items and combines them together
        for i, item in enumerate(self.inventory):
            [j.pick_up(item) for j in self.inventory[:i] if j is not None]

        # This removes any items in the inventory that have a quantity of 0 and replaces them with None
        remove: list[int] = [x[0] for x in enumerate(self.inventory) if x[1] is not None and x[1].quantity == 0]
        for i in remove:
            self.inventory[i] = None

    def drop_held_item(self) -> Item | None:
        """
        Call this method when a station is taking the held item from the avatar.

        ----

        This method can be modified more for different scenarios where the held item would be dropped
            (e.g., you make a game where being attacked forces you to drop your held item).

        ----

        If you want the held item to go somewhere specifically and not become None, that can be changed too.

        ----

        Make sure to keep clean inventory in this method.
        """
        # The held item will be taken from the avatar will be replaced with None in the inventory
        held_item = self.held_item
        self.inventory[self.__held_index] = None

        self.__clean_inventory()

        return held_item

    def take(self, item: Item | None) -> Item | None:
        """
        To use this method, pass in an item object. Whatever this item's quantity is will be the amount subtracted from
            the avatar's inventory. For example, if the item in the inventory is has a quantity of 5 and this method is
            called with the parameter having a quantity of 2, the item in the inventory will have a quantity of 3.

        ----

        Furthermore, when this method is called and the potential item is taken away, the clean_inventory method is
            called. It will consolidate all similar items together to ensure that the inventory is clean.

        ----

        Reference test_avatar_inventory.py and the clean_inventory method for further documentation on this method and
            how the inventory is managed.

        ----

        :param item:
        :return: Item or None
        """
        # Calls the take method on every index on the inventory. If i isn't None, call the method
        # NOTE: If the list is full of None (i.e., no Item objects are in it), nothing will happen
        [item := i.take(item) for i in self.inventory if i is not None]
        self.__clean_inventory()
        return item

    def pick_up(self, item: Item | None) -> Item | None:
        self.__clean_inventory()

        # Calls the pick_up method on every index on the inventory. If i isn't None, call the method
        [item := i.pick_up(item) for i in self.inventory if i is not None]

        # If the inventory has a slot with None, it will replace that None value with the item
        if self.inventory.__contains__(None):
            index = self.inventory.index(None)
            self.inventory.pop(index)
            self.inventory.insert(index, item)
            # Nothing is then returned
            return None

        # If the item can't be in the inventory, return it
        return item
