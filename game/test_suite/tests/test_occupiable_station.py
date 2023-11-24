import unittest

from game.common.items.item import Item
from game.common.map.wall import Wall
from game.common.stations.station import Station
from game.quarry_rush.station.ore_occupiable_stations import *


class TestOccupiableStation(unittest.TestCase):
    """
    `Test Item Notes:`

        This class tests the different methods in the OccupiableStation class and ensures the objects that occupy them
        are properly set.
    """

    def setUp(self) -> None:
        self.occupiable_station: OccupiableStation = OccupiableStation()
        self.occupiable_station1: OccupiableStation = OccupiableStation()
        self.wall: Wall = Wall()
        self.station: Station = Station()
        self.avatar: Avatar = Avatar()
        self.item: Item = Item()

    # test adding wall to occupiable_station
    def test_wall_occ(self):
        self.occupiable_station.occupied_by = self.wall
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.WALL)

    # test adding station to occupiable_station
    def test_station_occ(self):
        self.occupiable_station.occupied_by = self.station
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.STATION)

    # test adding avatar to occupiable_station
    def test_avatar_occ(self):
        self.occupiable_station.occupied_by = self.avatar
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.AVATAR)

    # test adding item to occupiable_station
    def test_item_occ(self):
        self.occupiable_station.item = self.item
        self.assertEqual(self.occupiable_station.item.object_type, ObjectType.ITEM)
        self.assertEqual(self.occupiable_station.item.durability, self.item.durability)
        self.assertEqual(self.occupiable_station.item.value, self.item.value)

    # test cannot add item to occupied_by
    def test_fail_item_occ(self):
        with self.assertRaises(ValueError) as e:
            self.occupiable_station.occupied_by = self.item
        self.assertEqual(str(e.exception), 'OccupiableStation.occupied_by cannot be an Item.')

    # test json method
    def test_occ_json(self):
        self.occupiable_station.occupied_by = self.avatar
        data: dict = self.occupiable_station.to_json()
        occupiable_station: OccupiableStation = OccupiableStation().from_json(data)
        self.assertEqual(self.occupiable_station.object_type, occupiable_station.object_type)
        self.assertEqual(self.occupiable_station.occupied_by.object_type, occupiable_station.occupied_by.object_type)

    # test json method with nested occupiable_station
    def test_nested_occ_json(self):
        self.occupiable_station.occupied_by = self.occupiable_station1
        self.occupiable_station.occupied_by.occupied_by = self.avatar
        data: dict = self.occupiable_station.to_json()
        occupiable_station: OccupiableStation = OccupiableStation().from_json(data)
        self.assertEqual(self.occupiable_station.object_type, occupiable_station.object_type)
        self.assertEqual(self.occupiable_station.occupied_by.object_type, occupiable_station.occupied_by.object_type)
        assert (isinstance(occupiable_station.occupied_by, OccupiableStation))
        self.assertEqual(self.occupiable_station.occupied_by.occupied_by.object_type,
                         occupiable_station.occupied_by.occupied_by.object_type)
