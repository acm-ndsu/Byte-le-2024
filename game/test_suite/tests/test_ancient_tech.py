import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.items.ancient_tech import Ancient_Tech
from game.utils.vector import Vector
from game.common.enums import ObjectType


class TestAncientTech(unittest.TestCase):
    """
    This class is to test the AncientTech class and its methods.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar(None, 1)
        self.Ancient_Tech: Ancient_Tech = Ancient_Tech()

   