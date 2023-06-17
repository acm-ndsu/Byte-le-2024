import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.items.ancient_tech import Ancient_Tech
from game.common.enums import Company


class TestAncientTech(unittest.TestCase):
    """
    This class is to test the AncientTech class and its methods.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar()
        self.Ancient_Tech: Ancient_Tech = Ancient_Tech()