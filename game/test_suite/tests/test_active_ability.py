import unittest
from game.quarry_rush.active_ability import ActiveAbility
from game.common.game_object import GameObject


class TestActiveAbility(unittest.TestCase):

    """
    This is class that tests the Active Ability
    """

    def setUp(self) -> None:
        self.active_ability = ActiveAbility
        self.name: str = ""
        self.cooldown: int = 1

    # test name
    def test_name(self):
        # if it is a string it passes
        self.name = ""
        self.active_ability.name = ""
        self.assertEqual(self.active_ability.name, self.name)

    # test name CANT be null
    def test_name_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.name = None
        self.assertEqual(str(e.exception), 'ActiveAbility.name must be a String')

    # test name cant be anything else
    def test_name_fail_int(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.name = 5
        self.assertEqual(str(e.exception), 'ActiveAbility.name must be a String')

    # test cooldown
    def test_cooldown(self):
        self.cooldown = 1
        self.active_ability.cooldown = 1
        self.assertEqual(self.active_ability.cooldown, self.cooldown)

    # test cooldown CANT be null
    def test_cooldown_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.cooldown = None
        self.assertEqual(str(e.exception), 'ActiveAbility.cooldown must be an int')

    # test cooldown cant be anything else
    def test_cooldown_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.cooldown = "ya mums gae"
        self.assertEqual(str(e.exception), 'ActiveAbility.cooldown must be an int')

    # test json
    def test_active_ability_json(self):
        data = self.active_ability.to_json()
        active_ability = ActiveAbility.from_json(data)
        self.assertEqual(self.active_ability.name, active_ability.name)
        self.assertEqual(self.active_ability.cooldown, active_ability.cooldown)




