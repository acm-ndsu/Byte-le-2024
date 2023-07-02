import unittest
from game.quarry_rush.dynamite_item import DynamiteItem
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.utils.vector import Vector
from game.common.enums import ObjectType


class TestDynamiteItem(unittest.TestCase):
    """
    This is a class that tests the class dynamite item
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar()
        self.dynamite_item: DynamiteItem = DynamiteItem()

    # test inventory manager

    # test value
    def test_value(self):
        self.value = 1
        self.dynamite_item.value = self.value
        self.assertEqual(self.dynamite_item.value, self.value)



