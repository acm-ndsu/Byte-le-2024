import unittest

from game.quarry_rush.entity.ore import Ore


class TestOre(unittest.TestCase):
    """
    This class is here to test the Ore class.
    """

    def setUp(self) -> None:
        self.ore: Ore = Ore()

    def test_ore(self) -> None:
        self.assertEqual(Ore().object_type, self.ore.object_type)

