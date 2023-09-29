import unittest

from game.quarry_rush.entity.ancient_tech import AncientTech


class TestAncientTech(unittest.TestCase):
    """
    This class is here to test the AncientTech class.
    """

    def setUp(self) -> None:
        self.ancient_tech: AncientTech = AncientTech()

    def test_ancient_tech(self) -> None:
        self.assertEqual(AncientTech().object_type, self.ancient_tech.object_type)


