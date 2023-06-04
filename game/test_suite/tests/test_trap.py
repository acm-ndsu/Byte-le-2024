import unittest

from game.quarry_rush.traps.trap import Trap
from game.common.avatar import Avatar

class TestTrap(unittest.TestCase):
    """
    This class is to test the generic trap class and its methods for the Byte-le 2024 game
    """

    def setUp(self) -> None:
        self.avatar = Avatar(None)
        self.avatar2 = Avatar(None)
        self.trap: Trap = Trap(False, 0.0, 0.0, self.avatar, 1, None, 1, 1, None, 'trap')
    
    # test set activated bool
    def test_set_activated(self):
        self.trap.activated = True
        self.assertEqual(self.trap.activated, True)
    
    def test_set_activated_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.trap.activated = None
        self.assertEqual(str(e.exception), 'Trap.activated must be a bool.')

    def test_set_activated_fail(self):
        with self.assertRaises(ValueError) as e:
            self.trap.activated = 10
        self.assertEqual(str(e.exception), 'Trap.activated must be a bool.')

    # test set detection_reduction
    def test_set_detection_reduction(self):
        self.trap.detection_reduction = 0.1
        self.assertEqual(self.trap.detection_reduction, 0.1)

    def test_set_detection_reduction_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.trap.detection_reduction = None
        self.assertEqual(str(e.exception), 'Trap.detection_reduction must be a float.')

    def test_set_detection_reduction_fail(self):
        with self.assertRaises(ValueError) as e:
            self.trap.detection_reduction = 1
        self.assertEqual(str(e.exception), 'Trap.detection_reduction must be a float.')

    # test set steal_rate
    def test_set_steal_rate(self):
        self.trap.steal_rate = 0.1
        self.assertEqual(self.trap.steal_rate, 0.1)

    def test_set_steal_rate_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.trap.steal_rate = None
        self.assertEqual(str(e.exception), 'Trap.steal_rate must be a float.')

    def test_set_steal_rate_fail(self):
        with self.assertRaises(ValueError) as e:
            self.trap.steal_rate = 1
        self.assertEqual(str(e.exception), 'Trap.steal_rate must be a float.')
    
    # test set owner
    def test_set_owner(self):
        self.trap.owner = self.avatar2
        self.assertEqual(self.trap.owner, self.avatar2)
    
    def test_set_owner_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.trap.owner = None
        self.assertEqual(str(e.exception), 'Trap.owner must be of type Avatar.')

    def test_set_owner_fail(self):
        with self.assertRaises(ValueError) as e:
            self.trap.owner = 'avatar'
        self.assertEqual(str(e.exception), 'Trap.owner must be of type Avatar.')

    # test json
    def test_trap_json(self):
        data: dict = self.trap.to_json()
        """ 
        Using from_json in the trap class requires four arguments to be passed, though they are not 
        used in the from_json method and do not need to match, as long as they fit value type required.
        """
        trap: Trap = Trap(False, 0.1, 0.1, self.avatar2).from_json(data)
        self.assertEqual(self.trap.object_type, trap.object_type)
        self.assertEqual(self.trap.activated, trap.activated)
        self.assertEqual(self.trap.detection_reduction, trap.detection_reduction)
        self.assertEqual(self.trap.steal_rate, trap.steal_rate)

