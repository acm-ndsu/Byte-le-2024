import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.utils.vector import Vector


class TestAvatarInventory(unittest.TestCase):
    """
    This class is to test the Avatar class' inventory and how it functions.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar(None, None, 1)
        self.item: Item = Item(10, 100, 1, 1)
