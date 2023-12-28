import unittest
from game.quarry_rush.ability.trap_defusal_active_ability import TrapDefusalActiveAbility


class TestTrapDefusalActiveAbility(unittest.TestCase):
    """
    This is class that tests the Trap Defusal Active Ability
    """
    
    # set up
    def setUp(self) -> None:
        self.trap_defusal_active_ability: TrapDefusalActiveAbility = TrapDefusalActiveAbility()

    # test: cooldown
    def test_cooldown(self):
        self.trap_defusal_active_ability.cooldown = 1
        self.assertEqual(self.trap_defusal_active_ability.cooldown, 1)

    # fail test: cooldown CANT be null
    def test_cooldown_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.trap_defusal_active_ability.cooldown = None
        self.assertEqual(str(e.exception), 'TrapDefusalActiveAbility.cooldown must be an int')

    # fail test: cooldown cant be anything else
    def test_cooldown_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.trap_defusal_active_ability.cooldown = ""
        self.assertEqual(str(e.exception), 'TrapDefusalActiveAbility.cooldown must be an int')

    # fail test: cooldown cannot be negative
    def test_cooldown_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.trap_defusal_active_ability.cooldown = -1
        self.assertEqual(str(e.exception), 'TrapDefusalActiveAbility.cooldown cannot be negative')

    # test: fuse
    def test_fuse(self):
        self.fuse = 1
        self.trap_defusal_active_ability.fuse = 1
        self.assertEqual(self.trap_defusal_active_ability.fuse, self.fuse)

    # fail test: fuse CANT be null
    def test_fuse_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.trap_defusal_active_ability.fuse = None
        self.assertEqual(str(e.exception), 'TrapDefusalActiveAbility.fuse must be an int')

    # fail test: fuse cannot be anything else
    def test_fuse_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.trap_defusal_active_ability.fuse = ""
        self.assertEqual(str(e.exception), 'TrapDefusalActiveAbility.fuse must be an int')

    # fail test: fuse cannot be negative
    def test_fuse_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.trap_defusal_active_ability.fuse = -1
        self.assertEqual(str(e.exception), 'TrapDefusalActiveAbility.fuse cannot be negative')

    # test: json
    def test_trap_defusal_active_ability_json(self):
        data: dict = self.trap_defusal_active_ability.to_json()
        trap_defusal_active_ability: TrapDefusalActiveAbility = TrapDefusalActiveAbility().from_json(data)
        self.assertEqual(self.trap_defusal_active_ability.cooldown, trap_defusal_active_ability.cooldown)
        self.assertEqual(self.trap_defusal_active_ability.fuse, trap_defusal_active_ability.fuse)
        self.assertEqual(self.trap_defusal_active_ability.object_type, trap_defusal_active_ability.object_type)
