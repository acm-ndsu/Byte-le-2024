import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.utils.vector import Vector


# class to test the avatar class and its methods
class TestAvatar(unittest.TestCase):
    def setUp(self) -> None:
        self.avatar: Avatar = Avatar(None, None, [], 1)
        self.item: Item = Item(10, 100, 1, 1)

    # test set item
    def test_avatar_set_item(self):
        self.avatar.held_item = self.item
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

    def test_avatar_set_position_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.position = 10
        self.assertEqual(str(e.exception), 'Avatar.position must be a Vector or None.')

    # test set inventory
    def test_avatar_set_inventory(self):
        self.avatar.inventory = [Item(1, 1)]
        self.assertEqual(self.avatar.inventory[0].value, Item(1, 1).value)

    # fails if inventory is not a list
    def test_avatar_set_inventory_fail_1(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.inventory = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.inventory must be a list of Items.')

    # fails if inventory size is less than the max_inventory_size
    def test_avatar_set_inventory_fail_2(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.inventory = [Item(1, 1), Item(4, 2)]
        self.assertEqual(str(e.exception), 'Avatar.inventory size must be less than max_inventory_size')

    def test_avatar_set_max_inventory_size(self):
        self.avatar.max_inventory_size = 10
        self.assertEqual(str(self.avatar.max_inventory_size), str(10))

    def test_avatar_set_max_inventory_size_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.max_inventory_size = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.max_inventory_size must be an int.')

        # test json method

    def test_avatar_json(self):
        self.avatar.held_item = self.item
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.held_item.object_type, avatar.held_item.object_type)
        self.assertEqual(self.avatar.held_item.value, avatar.held_item.value)
        self.assertEqual(self.avatar.held_item.durability, avatar.held_item.durability)
        self.assertEqual(self.avatar.position.object_type, avatar.position.object_type)
        self.assertEqual(str(self.avatar.position), str(avatar.position))
