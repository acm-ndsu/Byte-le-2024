import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.utils.vector import Vector

# class to test the avatar class and its methods
class TestAvatar(unittest.TestCase):
    def setUp(self) -> None:
        self.item: Item = Item(10, 100)
        self.avatar: Avatar = Avatar(None, None)
        
    # test set item
    def testAvatarSetItem(self):
        self.avatar.held_item = self.item
        self.assertEqual(self.avatar.held_item, self.item)

    def testAvatarSetItemFail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.held_item = 3
        self.assertEqual(str(e.exception), 'Avatar.held_item must be an Item or None.')

    # test set score
    def testAvatarSetScore(self):
        self.avatar.score = 10
        self.assertEqual(self.avatar.score, 10)

    def testAvatarSetScoreFail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.score = 'wow'
        self.assertEqual(str(e.exception), 'Avatar.score must be an int.')

    # test set position
    def testAvatarSetPosition(self):
        self.avatar.position = Vector(10,10)
        self.assertEqual(str(self.avatar.position), str(Vector(10,10)))

    def testAvatarSetPositionFail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.position = 10
        self.assertEqual(str(e.exception), 'Avatar.position must be a Vector or None.')

    # test json method
    def testAvatarJson(self):
        self.avatar.held_item = self.item
        self.avatar.position = Vector(10,10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.held_item.object_type, avatar.held_item.object_type)
        self.assertEqual(self.avatar.held_item.value, avatar.held_item.value)
        self.assertEqual(self.avatar.held_item.durability, avatar.held_item.durability)
        self.assertEqual(self.avatar.position.object_type, avatar.position.object_type)
        self.assertEqual(str(self.avatar.position), str(avatar.position))
