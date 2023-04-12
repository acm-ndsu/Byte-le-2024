import unittest

from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.common.stations.station import Station
from game.common.stations.occupiable_station import Occupiable_Station
from game.common.avatar import Avatar
from game.common.enums import ObjectType

# class that tests the tile class and its methods
class TestTile(unittest.TestCase):
    def setUp(self) -> None:
        self.tile: Tile = Tile()
        self.wall: Wall = Wall()
        self.station: Station = Station()
        self.occupiable_station: Occupiable_Station = Occupiable_Station()
        self.avatar: Avatar = Avatar()

    # test adding avatar to tile
    def testAvatarTile(self):
        self.tile.occupied_by = self.avatar
        self.assertEqual(self.tile.occupied_by.object_type, ObjectType.AVATAR)

    # test adding station to tile
    def testStationTile(self):
        self.tile.occupied_by = self.station
        self.assertEqual(self.tile.occupied_by.object_type, ObjectType.STATION)
    
    # test adding occupiable_station to tile
    def testOccupiable_StationTile(self):
        self.tile.occupied_by = self.occupiable_station
        self.assertEqual(self.tile.occupied_by.object_type, ObjectType.OCCUPIABLE_STATION)

    # test aadding wall to tile
    def testWallTile(self):
        self.tile.occupied_by = self.wall
        self.assertEqual(self.tile.occupied_by.object_type, ObjectType.WALL)

    # test json method
    def testTileJson(self):
        self.tile.occupied_by = self.station
        data: dict = self.tile.to_json()
        tile: Tile = Tile().from_json(data)
        self.assertEqual(self.tile.object_type, tile.object_type)
        self.assertEqual(self.tile.occupied_by.object_type, tile.occupied_by.object_type)

    # test if json is correct when nested tile
    def testNestedTileJson(self):
        self.occupiable_station.occupied_by = self.avatar
        self.tile.occupied_by = self.occupiable_station
        data: dict = self.tile.to_json()
        tile: Tile = Tile().from_json(data)
        self.assertEqual(self.tile.object_type, tile.object_type)
        self.assertEqual(self.tile.occupied_by.object_type, tile.occupied_by.object_type)
        assert(isinstance(tile.occupied_by, Occupiable_Station))
        self.assertEqual(self.tile.occupied_by.occupied_by.object_type, tile.occupied_by.occupied_by.object_type)