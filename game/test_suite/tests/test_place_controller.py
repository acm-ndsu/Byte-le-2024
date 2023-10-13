import unittest

from numpy import place

from game.controllers.movement_controller import *
from game.controllers.place_controller import *
from game.quarry_rush.station.ore_occupiable_stations import *
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.traps import *


class TestPlaceController(unittest.TestCase):
    """
    This class is to test the TestPlaceController and placing Dynamite, Landmines, and EMPs on the GameBoard
    """

    def setUp(self) -> None:

        # Make controller objects for testing
        self.place_controller: PlaceController = PlaceController()
        self.movement_controller: MovementController = MovementController()

        self.avatar = Avatar(position=Vector(1, 0))
        self.copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        self.lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        self.turite_station: TuriteOccupiableStation = TuriteOccupiableStation()

        # stack copium, lambdium, then turite; turite on top (i.e., copium -> lambium -> turite)
        self.lambdium_station.occupied_by = self.turite_station
        self.copium_station.occupied_by = self.lambdium_station

        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1),): [self.copium_station],
            (Vector(1, 0),): [self.avatar]
        }

        self.game_board = GameBoard(0, Vector(3, 3), self.locations, False)

        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

    # tests that the avatar is at the top of the stack
    def test_avatar_on_top_of_ores(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)  # move to position
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 1)))  # ensure position is fine
        self.assertEqual(self.turite_station.occupied_by, self.client.avatar)  # ensure avatar is on top
        self.assertNotEqual(self.lambdium_station.occupied_by, self.client.avatar)  # ensure avatar is not on lambdium
        self.assertNotEqual(self.copium_station.occupied_by, self.client.avatar)  # ensure avatar is not on copium

    def test_placing_dynamite(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.client, self.game_board)

        # ensuring the stack is in the order it should be in
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)

        # test if the turite is occupied by a Dynamite object and not the avatar
        self.assertEqual(isinstance(self.turite_station.occupied_by, Dynamite), True)
        self.assertNotEqual(self.turite_station.occupied_by, self.client.avatar)

        # test if Dynamite is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_dyn: Dynamite = self.turite_station.occupied_by  # returns the correct type
        self.assertEqual(placed_dyn.occupied_by, self.client.avatar)

    def test_placing_landmine(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_LANDMINE, self.client, self.game_board)

        # ensuring the stack is in the order it should be in
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)

        # test if the turite is occupied by a Dynamite object and not the avatar
        self.assertEqual(isinstance(self.turite_station.occupied_by, Dynamite), True)
        self.assertNotEqual(self.turite_station.occupied_by, self.client.avatar)

        # test if Dynamite is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_landmine: Landmine = self.turite_station.occupied_by  # returns the correct type
        self.assertEqual(placed_landmine.occupied_by, self.client.avatar)

    def test_placing_emp(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_LANDMINE, self.client, self.game_board)

        # ensuring the stack is in the order it should be in
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)

        # test if the turite is occupied by a Dynamite object and not the avatar
        self.assertEqual(isinstance(self.turite_station.occupied_by, Dynamite), True)
        self.assertNotEqual(self.turite_station.occupied_by, self.client.avatar)

        # test if Dynamite is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_emp: EMP = self.turite_station.occupied_by  # returns the correct type
        self.assertEqual(placed_emp.occupied_by, self.client.avatar)
