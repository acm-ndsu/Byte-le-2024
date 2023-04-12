import unittest

from game.common.stations.occupiable_station import Occupiable_Station
from game.common.stations.station import Station
from game.common.map.wall import Wall
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.enums import ObjectType

# class that tests occupiable_station and its methods
class TestOccupiable_Station(unittest.TestCase):
    def setUp(self) -> None:
        self.occupiable_station: Occupiable_Station = Occupiable_Station()
        self.occupiable_station1: Occupiable_Station = Occupiable_Station()
        self.wall: Wall = Wall()
        self.station: Station = Station()
        self.avatar: Avatar = Avatar()
        self.item: Item = Item()
    
    # test adding wall to occupiable_station
    def testWallOcc(self):
        self.occupiable_station.occupied_by = self.wall
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.WALL)
    
    # test adding station to occupiable_station
    def testStationOcc(self):
        self.occupiable_station.occupied_by = self.station
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.STATION)
    
    # test adding avatar to occupiable_station
    def testAvatarOcc(self):
        self.occupiable_station.occupied_by = self.avatar
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.AVATAR)

    # test adding item to occupiable_station
    def testItemOcc(self):
        self.occupiable_station.item = self.item
        self.assertEqual(self.occupiable_station.item.object_type, ObjectType.ITEM)
        self.assertEqual(self.occupiable_station.item.durability, self.item.durability)
        self.assertEqual(self.occupiable_station.item.value, self.item.value)

    # test cannot add item to occupied_by
    def testFailItemOcc(self):
        with self.assertRaises(ValueError) as e:
            self.occupiable_station.occupied_by = self.item
        self.assertEqual(str(e.exception), 'Occupiable_Station.occupied_by cannot be an Item.')

    # test json method
    def testOccJson(self):
        self.occupiable_station.occupied_by = self.avatar
        data: dict = self.occupiable_station.to_json()
        occupiable_station: Occupiable_Station = Occupiable_Station().from_json(data)
        self.assertEqual(self.occupiable_station.object_type, occupiable_station.object_type)
        self.assertEqual(self.occupiable_station.occupied_by.object_type, occupiable_station.occupied_by.object_type)
    
    # test json method with nested occupiable_station
    def testNestedOccJson(self):
        self.occupiable_station.occupied_by = self.occupiable_station1
        self.occupiable_station.occupied_by.occupied_by = self.avatar
        data: dict = self.occupiable_station.to_json()
        occupiable_station: Occupiable_Station = Occupiable_Station().from_json(data)
        self.assertEqual(self.occupiable_station.object_type, occupiable_station.object_type)
        self.assertEqual(self.occupiable_station.occupied_by.object_type, occupiable_station.occupied_by.object_type)
        assert(isinstance(occupiable_station.occupied_by, Occupiable_Station))
        self.assertEqual(self.occupiable_station.occupied_by.occupied_by.object_type, occupiable_station.occupied_by.occupied_by.object_type)