import unittest
from game.quarry_rush.dynamite_active_ability import DynamiteActiveAbility
from game.utils.vector import Vector


class TestDynamiteActiveAbility(unittest.TestCase):

    """
    This is class that tests the Active Ability
    """
    # set up
    def setUp(self) -> None:
        self.dynamite_active_ability = DynamiteActiveAbility()
        self.name: str = ""
        self.cooldown: int = 1

    # test: name
    def test_name(self):
        self.name = ""
        self.dynamite_active_ability.name = ""
        self.assertEqual(self.dynamite_active_ability.name, self.name)

    # fail test: name CANT be null
    def test_name_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.name = None
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.name must be a String')

    # fail test: name cant be anything else
    def test_name_fail_int(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.name = 1
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.name must be a String')

    # test: cooldown
    def test_cooldown(self):
        self.cooldown = 1
        self.dynamite_active_ability.cooldown = 1
        self.assertEqual(self.dynamite_active_ability.cooldown, self.cooldown)

    # fail test: cooldown CANT be null
    def test_cooldown_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown = None
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown must be an int')

    # fail test: cooldown cant be anything else
    def test_cooldown_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown = ""
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown must be an int')

    # fail test: cooldown cannot be negative
    def test_cooldown_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown = -1
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown cannot be negative')

    # test: cooldown_tick
    def test_cooldown_tick(self):
        self.cooldown_tick = 1
        self.dynamite_active_ability.cooldown_tick = 1
        self.assertEqual(self.dynamite_active_ability.cooldown_tick, self.cooldown_tick)

    # fail test: cooldown_tick CANT be null
    def test_cooldown_tick_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown_tick = None
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown_tick must be an int')

    # fail test: cooldown_tick cannot be anything else
    def test_cooldown_tick_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown_tick = ""
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown_tick must be an int')

    # fail test: cooldown_tick cannot be negative
    def test_cooldown_tick_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown_tick = -1
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown_tick cannot be negative')

    # test: position
    def test_dynamite_active_ability_set_position(self):
        self.dynamite_active_ability.position = Vector(10, 10)
        self.assertEqual(str(self.dynamite_active_ability.position), str(Vector(10, 10)))

    # test: position none
    def test_dynamite_active_ability_set_position_None(self):
        self.dynamite_active_ability.position = None
        self.assertEqual(self.dynamite_active_ability.position, None)

    # fail test: position cannot be anything else
    def test_dynamite_active_ability_set_position_fail(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.position = 10
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.position must be a Vector or None.')

    # test: for placing dynamite
    def test_placing_dynamite(self):
        self.dynamite_active_ability.placing_dynamite = False
        self.assertEqual(self.dynamite_active_ability.placing_dynamite, False)

    # fail test: placing dynamite cant be none
    def test_placing_dynamite_none_fail(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.placing_dynamite = None
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.placing_dynamite must be a bool.')

    # fail test: placing dynamite cant be anything else
    def test_placing_dynamite_str_fail(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.placing_dynamite = None
        self.assertEqual(str(e.exception), "DynamiteActiveAbility.placing_dynamite must be a bool.")

    # test: json
    def test_dynamite_active_ability_json(self):
        data: dict = self.dynamite_active_ability.to_json()
        dynamite_active_ability: DynamiteActiveAbility = DynamiteActiveAbility().from_json(data)
        self.assertEqual(self.dynamite_active_ability.name, dynamite_active_ability.name)
        self.assertEqual(self.dynamite_active_ability.cooldown, dynamite_active_ability.cooldown)
        self.assertEqual(self.dynamite_active_ability.cooldown_tick, dynamite_active_ability.cooldown_tick)
        self.assertEqual(self.dynamite_active_ability.object_type, dynamite_active_ability.object_type)
        self.assertEqual(str(self.dynamite_active_ability.position), str(dynamite_active_ability.position))




