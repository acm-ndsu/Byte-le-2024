import unittest
from game.quarry_rush.ability.place_trap import PlaceTrap
from game.common.avatar import Avatar


class TestPlaceTrap(unittest.TestCase):

    """
    This tests the place trap class
    """

    # set up
    def setUp(self) -> None:
        self.place_trap = PlaceTrap()
        self.cooldown: int = 1
        self.cooldown_tick: int = 1

    # test cooldown
    def test_cooldown(self):
        self.cooldown = 1
        self.place_trap.cooldown = 1
        self.assertEqual(self.place_trap.cooldown, self.cooldown)

    # fail test cooldown cant be None
    def fail_test_cooldown_null(self):
        with self.assertRaises(ValueError) as e:
            self.place_trap.cooldown = None
        self.assertEqual(str(e.exception), 'PlaceTrap.cooldown must be an int')

    # fail test cooldown cant be anything else
    def fail_test_cooldown_str(self):
        with self.assertRaises(ValueError) as e:
            self.place_trap.cooldown = ""
        self.assertEqual(str(e.exception), 'PlaceTrap.cooldown must be an int')

    # fail test cooldown cant be negative
    def fail_test_cooldown_negative(self):
        with self.assertRaises(ValueError) as e:
            self.place_trap.cooldown = -1
        self.assertEqual(str(e.exception), 'PlaceTrap.cooldown must be positive')

    # test cooldown tick
    def test_cooldown_tick(self):
        self.cooldown_tick = 1
        self.place_trap.cooldown_tick = 1
        self.assertEqual(self.place_trap.cooldown_tick, self.cooldown_tick)

    # fail test cooldown tick null
    def fail_test_cooldown_tick_null(self):
        with self.assertRaises(ValueError) as e:
            self.place_trap.cooldown_tick = None
        self.assertEqual(str(e.exception), 'PlaceTrap.cooldown_tick must be an int')

    # fail test cooldown tick cant be anything else
    def fail_test_cooldown_tick_str(self):
        with self.assertRaises(ValueError) as e:
            self.place_trap.cooldown_tick = ""
        self.assertEqual(str(e.exception), 'PlaceTrap.cooldown_tick must be an int')

    # fail test cooldown tick cant be negative
    def fail_test_cooldown_tick_negative(self):
        with self.assertRaises(ValueError) as e:
            self.place_trap.cooldown_tick = -1
        self.assertEqual(str(e.exception), 'PlaceTrap.cooldown_tick must be positive')

    # test avatar
    def test_avatar(self):
        self.avatar = Avatar()
        self.place_trap.avatar = self.avatar
        self.assertEqual(self.place_trap.avatar, self.avatar)

    # test avatar none
    def test_avatar_none(self):
        self.avatar = None
        self.place_trap.avatar = self.avatar
        self.assertEqual(self.place_trap.avatar, self.avatar)

    # fail test avatar cant be anything else
    def fail_test_avatar_str(self):
        with self.assertRaises(ValueError) as e:
            self.place_trap.avatar = ""
        self.assertEqual(str(e.exception), 'PlaceTrap.avatar must be None or Avatar')

    # testing the json
    def test_json(self):
        data: dict = self.place_trap.to_json()
        place_trap: PlaceTrap = PlaceTrap().from_json(data)
        self.assertEqual(self.place_trap.object_type, place_trap.object_type)
        self.assertEqual(self.place_trap.placing_trap, place_trap.placing_trap)
        self.assertEqual(self.place_trap.cooldown, place_trap.cooldown)
        self.assertEqual(self.place_trap.cooldown_tick, place_trap.cooldown_tick)
