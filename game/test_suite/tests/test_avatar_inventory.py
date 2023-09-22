import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item


class TestAvatarInventory(unittest.TestCase):
    """
    `Test Avatar Inventory Notes:`

        This class tests the different methods in the Avatar class related to the inventory system. This is its own
        file since the inventory system has a lot of functionality. Look extensively at the different cases that are
        tested to better understand how it works if there is still confusion.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar()
        self.item: Item = Item(10, 100, 1, 1)
