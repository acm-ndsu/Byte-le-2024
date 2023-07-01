import unittest
from game.quarry_rush.dynamite_item import DynamiteItem
from game.common.avatar import Avatar
from game.common.items.item import Item


class TestDynamiteItem(unittest.TestCase):
    """
    This is a class that tests the class dynamite item
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar()
        self.item: Item = Item()
