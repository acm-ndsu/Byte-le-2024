import unittest
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.utils.vector import Vector


# need to test collection method<-later, test inventory_manager<-later,  explode<-its own file
class TestDynamite(unittest.TestCase):
    """
    This is a class that tests the class dynamite item
    """

    def setUp(self) -> None:
        self.dynamite: Dynamite = Dynamite()
        self.blast_radius: int = 1
        self.detonate_turn: int = 1

    # test: position
    def test_dynamite_position(self):
        self.dynamite.position = Vector(10, 10)
        self.assertEqual(str(self.dynamite.position), str(Vector(10, 10)))

    # test: position none
    def test_dynamite_position_None(self):
        self.dynamite.position = None
        self.assertEqual(self.dynamite.position, None)

    # fail test: position cannot be anything else
    def fail_test_dynamite_position(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite.position = 10
        self.assertEqual(str(e.exception), 'Dynamite.position must be a Vector or None.')

    # test: blast radius can only be an int
    def test_blast_radius(self):
        self.dynamite.blast_radius = 1
        self.assertEqual(self.dynamite.blast_radius, self.blast_radius)

    # fail test: blast radius cannot be none
    def fail_test_blast_radius_none(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite.blast_radius = None
        self.assertEqual(str(e.exception), 'Dynamite.blast_radius must be an int.')

    # fail test: blast radius cannot be anything else
    def fail_Test_blast_radius_str(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite.blast_radius = ""
        self.assertEqual(str(e.exception), 'Dynamite.blast_radius must be an int.')

    # test: detonate_turn
    def test_detonate_turn(self):
        self.dynamite.detonate_turn = 1
        self.assertEqual(self.dynamite.detonate_turn, self.detonate_turn)

    # fail test: detonate turn cannot be none
    def fail_test_detonate_turn_none(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite.detonate_turn = None
        self.assertEqual(str(e.exception), 'Dynamite.blast_radius must be an int.')

    # fail test: detonate turn cannot be anything else
    def fail_test_detonate_turn_str(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite.detonate_turn = ""
        self.assertEqual(str(e.exception), 'Dynamite.blast_radius must be an int.')

    # test decrementing the fuse and if it can explode or not
    def test_dynamite_can_explode(self):
        self.assertFalse(self.dynamite.can_explode())

        self.dynamite.decrement_fuse()
        self.assertEqual(self.dynamite.fuse, 0)

        self.assertTrue(self.dynamite.can_explode())


    # test inventory manager - later

    # test: json
    def test_dynamite_json(self):
        data: dict = self.dynamite.to_json()
        dynamite: Dynamite = Dynamite().from_json(data)
        self.assertEqual(str(self.dynamite.position), str(dynamite.position))
        self.assertEqual(self.dynamite.blast_radius, dynamite.blast_radius)
        self.assertEqual(self.dynamite.object_type, dynamite.object_type)
