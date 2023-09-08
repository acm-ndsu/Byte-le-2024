import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard, TrapQueue
from game.quarry_rush.traps.trap import Landmine, EMP
from game.quarry_rush.inventory_manager import InventoryManager
from game.common.enums import Company


class TestGameBoard(unittest.TestCase):
    """
    This class is to test the GameBoard class and its methods with the map being generated.
    """

    def setUp(self) -> None:
        self.item: Item = Item(10)
        self.wall: Wall = Wall()
        self.avatar: Avatar = Avatar(position=Vector(5, 5))
        self.locations: dict[tuple[Vector]:list[GameObject]] = {
            (Vector(1, 1),): [Station(None)],
            (Vector(1, 2), Vector(1, 3)): [OccupiableStation(self.item), Station(None)],
            (Vector(5, 5),): [self.avatar],
            (Vector(5, 6),): [self.wall]
        }
        self.game_board: GameBoard = GameBoard(1, Vector(10, 10), self.locations, False)
        self.game_board.generate_map()

    # test that seed cannot be set after generate_map
    def test_seed_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.seed = 20
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')

    # test that map_size cannot be set after generate_map
    def test_map_size_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.map_size = Vector(1, 1)
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')

    # test that locations cannot be set after generate_map
    def test_locations_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = self.locations
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')

    # test that locations raises RuntimeError even with incorrect data type
    def test_locations_incorrect_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = Vector(1, 1)
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')

    # test that walled cannot be set after generate_map
    def test_walled_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.walled = False
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')

    # test that get_objects works correctly with stations
    def test_get_objects_station(self):
        stations: list[tuple[Vector, list[Station]]] = self.game_board.get_objects(ObjectType.STATION)
        self.assertTrue(all(map(lambda station: isinstance(station[1][0], Station), stations)))
        self.assertEqual(len(stations), 2)

    # test that get_objects works correctly with occupiable stations
    def test_get_objects_occupiable_station(self):
        occupiable_stations: list[tuple[Vector, list[OccupiableStation]]] = self.game_board.get_objects(ObjectType.OCCUPIABLE_STATION)
        self.assertTrue(
            all(map(lambda occupiable_station: isinstance(occupiable_station[1][0], OccupiableStation), occupiable_stations)))
        self.assertEqual(len(occupiable_stations), 1)

    # test that get_objects works correctly with avatar
    def test_get_objects_avatar(self):
        avatars: list[tuple[Vector, list[Avatar]]] = self.game_board.get_objects(ObjectType.AVATAR)
        self.assertTrue(all(map(lambda avatar: isinstance(avatar[1][0], Avatar), avatars)))
        self.assertEqual(len(avatars), 1)

    # test that get_objects works correctly with walls
    def test_get_objects_wall(self):
        walls: list[tuple[Vector, list[Wall]]] = self.game_board.get_objects(ObjectType.WALL)
        self.assertTrue(all(map(lambda wall: isinstance(wall[1][0], Wall), walls)))
        self.assertEqual(len(walls), 1)

    # test json method
    def test_game_board_json(self):
        data: dict = self.game_board.to_json()
        temp: GameBoard = GameBoard().from_json(data)
        for (k, v), (x, y) in zip(self.locations.items(), temp.locations.items()):
            for (i, j), (a, b) in zip(zip(k, v), zip(x, y)):
                self.assertEqual(i.object_type, a.object_type)
                self.assertEqual(j.object_type, b.object_type)
                
    def test_create_trap_queues(self):
        self.assertIsNotNone(self.game_board.church_trap_queue)
        self.assertIsNotNone(self.game_board.turing_trap_queue)
        
    def test_add_trap(self):
        trap_queue = TrapQueue()

        self.assertEqual(trap_queue.size(), 0)
        trap_queue.add_trap(Landmine(inventory_manager=InventoryManager(), owner_company=Company.CHURCH, target_company=Company.TURING, opponent_position=lambda : Vector(), position=Vector()))
        self.assertEqual(trap_queue.size(), 1)
        for i in range(0, 10):
            trap_queue.add_trap(Landmine(inventory_manager=InventoryManager(), owner_company=Company.CHURCH, target_company=Company.TURING, opponent_position=lambda : Vector(), position=Vector()))
        self.assertEqual(trap_queue.size(), 10)
        
    def test_trap_detonator_controller(self):
        self.game_board.turing_trap_queue.add_trap(Landmine(inventory_manager=InventoryManager(), owner_company=Company.TURING, target_company=Company.CHURCH, opponent_position=lambda : Vector(), position=Vector()))
        self.game_board.turing_trap_queue.add_trap(EMP(inventory_manager=InventoryManager(), owner_company=Company.TURING, target_company=Company.CHURCH, opponent_position=lambda : Vector(), position=Vector(4,7)))
        self.game_board.church_trap_queue.add_trap(Landmine(inventory_manager=InventoryManager(), owner_company=Company.CHURCH, target_company=Company.TURING, opponent_position=lambda : Vector(5,5), position=Vector()))
        self.assertEqual(self.game_board.turing_trap_queue.size(), 2)
        self.assertEqual(self.game_board.church_trap_queue.size(), 1)
        self.game_board.trap_detonation_control()
        self.assertEqual(self.game_board.turing_trap_queue.size(), 1)
        self.assertEqual(self.game_board.church_trap_queue.size(), 1)

        