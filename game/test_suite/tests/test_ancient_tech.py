import unittest

from game.common.avatar import Avatar
from game.quarry_rush.entity.ancient_tech import Ancient_Tech


class TestAncientTech(unittest.TestCase):
    """
    This class is to test the AncientTech class and its methods.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar()
        self.Ancient_Tech: Ancient_Tech = Ancient_Tech()