import unittest

from game.common.avatar import Avatar
from game.quarry_rush.entity.ore import Ore


class TestAncientTech(unittest.TestCase):
    """
    This class is to test the AncientTech class and its methods.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar()
        self.Ancient_Tech: Ore = Ore()
