import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.utils.vector import Vector


class TestAvatar(unittest.TestCase):
    """
    This class is to test the Avatar class and its methods.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar(None, 1)
        self.item: Item = Item(10, 100, 1, 1)

    # test set item
    def test_avatar_set_item(self):
        self.avatar.pick_up(self.item)
        self.assertEqual(self.avatar.held_item, self.item)

    def test_avatar_set_item_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.held_item = 3
        self.assertEqual(str(e.exception), 'Avatar.held_item must be an Item or None.')

    # test set score
    def test_avatar_set_score(self):
        self.avatar.score = 10
        self.assertEqual(self.avatar.score, 10)

    def test_avatar_set_score_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.score = 'wow'
        self.assertEqual(str(e.exception), 'Avatar.score must be an int.')

    # test set position
    def test_avatar_set_position(self):
        self.avatar.position = Vector(10, 10)
        self.assertEqual(str(self.avatar.position), str(Vector(10, 10)))

    def test_avatar_set_position_None(self):
        self.avatar.position = None
        self.assertEqual(self.avatar.position, None)

    def test_avatar_set_position_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.position = 10
        self.assertEqual(str(e.exception), 'Avatar.position must be a Vector or None.')

    # test json method
    def test_avatar_json_with_none_item(self):
        # held item will be None
        self.avatar.held_item = self.avatar.inventory[0]
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.held_item, avatar.held_item)
        self.assertEqual(str(self.avatar.position), str(avatar.position))

    def test_avatar_json_with_item(self):
        self.avatar.pick_up(Item(1, 1))
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.held_item.object_type, avatar.held_item.object_type)
        self.assertEqual(self.avatar.held_item.value, avatar.held_item.value)
        self.assertEqual(self.avatar.held_item.durability, avatar.held_item.durability)
        self.assertEqual(self.avatar.position.object_type, avatar.position.object_type)
        self.assertEqual(str(self.avatar.position), str(avatar.position))

    # Quarry Rush tests below ------------------------------------------------------------------------------------------

    # Test setting movement speed
    def test_avatar_set_movement_speed(self):
        self.avatar.movement_speed = 5
        self.assertEqual(self.avatar.movement_speed, 5)

    def test_avatar_set_movement_speed_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.movement_speed = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.movement_speed must be an int.')

    # Test setting drop rate
    def test_avatar_set_drop_rate(self):
        self.avatar.drop_rate = 5.3
        self.assertEqual(self.avatar.drop_rate, 5.3)

    def test_avatar_set_drop_rate_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.drop_rate = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.drop_rate must be a float.')

    # Test setting steal rate
    def test_avatar_set_steal_rate(self):
        self.avatar.steal_rate = 3.3
        self.assertEqual(self.avatar.steal_rate, 3.3)

    # Test setting the steal rate to an illegal value
    def test_avatar_set_steal_rate_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.steal_rate = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.steal_rate must be a float.')

