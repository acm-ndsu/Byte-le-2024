import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard

# class to test initalization of game_board
class TestGameBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.item: Item = Item(10, None)
        self.wall: Wall = Wall()
        self.avatar: Avatar = Avatar(None, Vector(5, 5))
        self.locations: dict[tuple[Vector]:list[GameObject]] = {
            (Vector(1, 1),):[Station(None)],
            (Vector(1, 2), Vector(1, 3)):[OccupiableStation(self.item), Station(None)],
            (Vector(5, 5),):[self.avatar],
            (Vector(5, 6),):[self.wall]
        }
        self.game_board: GameBoard = GameBoard(1, Vector(10, 10), self.locations, False)
    
    # test seed
    def test_seed(self):
        self.game_board.seed = 2
        self.assertEqual(self.game_board.seed, 2)

    def test_seed_fail(self):
        with self.assertRaises(ValueError) as e:
            self.game_board.seed = "False"
        self.assertEqual(str(e.exception), 'GameBoard.seed must be an integer or None.')

    # test map_size
    def test_map_size(self):
        self.game_board.map_size = Vector(12, 12)
        self.assertEqual(str(self.game_board.map_size), str(Vector(12, 12)))

    def test_map_size_fail(self):
        with self.assertRaises(ValueError) as e:
            self.game_board.map_size = "wow"
        self.assertEqual(str(e.exception), 'GameBoard.map_size must be a Vector.')

    # test locations
    def test_locations(self):
        self.locations = {
            (Vector(1, 1),):[self.avatar],
            (Vector(1, 2), Vector(1, 3)):[OccupiableStation(self.item), Station(None)],
            (Vector(5, 5),):[Station(None)],
            (Vector(5, 6),):[self.wall]
        }
        self.game_board.locations = self.locations
        self.assertEqual(str(self.game_board.locations), str(self.locations))

    def test_locations_fail_type(self):
        with self.assertRaises(ValueError) as e:
            self.game_board.locations = "wow"
        self.assertEqual(str(e.exception), 'Locations must be a dict. The key must be a tuple of Vector Objects, and the value a list of GameObject.')

    def test_locations_fail_len(self):
        with self.assertRaises(ValueError) as e:
            self.locations = {
            (Vector(1, 1),):[],
            (Vector(1, 2), Vector(1, 3)):[OccupiableStation(self.item), Station(None)],
            (Vector(5, 5),):[Station(None)],
            (Vector(5, 6),):[self.wall]
        }
            self.game_board.locations = self.locations
        self.assertEqual(str(e.exception), 'Cannot set the locations for the game_board. A key has a different length than its key.')

    # test walled
    def test_walled(self):
        self.game_board.walled = True
        self.assertEqual(self.game_board.walled, True)

    def test_walled_fail(self):
        with self.assertRaises(ValueError) as e:
            self.game_board.walled = "wow"
        self.assertEqual(str(e.exception), 'GameBoard.walled must be a bool.')

    # test json method
    def test_game_board_json(self):
        data: dict = self.game_board.to_json()
        temp: GameBoard = GameBoard().from_json(data)
        for (k, v), (x, y) in zip(self.locations.items(), temp.locations.items()):
            for (i, j), (a, b) in zip(zip(k, v), zip(x, y)):
                self.assertEqual(i.object_type, a.object_type)
                self.assertEqual(j.object_type, b.object_type)

    def test_generate_map(self):
        self.game_board.generate_map()
        self.assertEqual(self.game_board.game_map[1][1].occupied_by.object_type, ObjectType.STATION) 
        self.assertEqual(self.game_board.game_map[2][1].occupied_by.object_type, ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(self.game_board.game_map[3][1].occupied_by.object_type, ObjectType.STATION)
        self.assertEqual(self.game_board.game_map[5][5].occupied_by.object_type, ObjectType.AVATAR)
        self.assertEqual(self.game_board.game_map[6][5].occupied_by.object_type, ObjectType.WALL)