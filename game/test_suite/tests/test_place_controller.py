import unittest

from game.common.game_object import GameObject
from game.controllers.movement_controller import *
from game.controllers.place_controller import *
from game.quarry_rush.station.ore_occupiable_station import *
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

        # Unlock the entire tech tree for testing
        self.avatar.buy_new_tech('Better Drivetrains')
        self.avatar.buy_new_tech('Unnamed Drivetrain Tech')
        self.avatar.buy_new_tech('Overdrive Movement')
        self.avatar.buy_new_tech('High Yield Drilling')
        self.avatar.buy_new_tech('Unnamed Mining Tech')
        self.avatar.buy_new_tech('Dynamite')
        self.avatar.buy_new_tech('Landmines')
        self.avatar.buy_new_tech('EMPs')
        self.avatar.buy_new_tech('Trap Defusal')

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
        self.assertTrue(isinstance(self.turite_station.occupied_by, Dynamite))
        self.assertNotEqual(self.turite_station.occupied_by, self.client.avatar)

        # test if Dynamite is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_dyn: Dynamite = self.turite_station.occupied_by  # returns the correct type; ignore warning
        self.assertEqual(placed_dyn.occupied_by, self.client.avatar)

        self.assertEqual(self.avatar.dynamite_active_ability.cooldown, 1)  # double-check the ability cooldown reset

    def test_placing_landmine(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_LANDMINE, self.client, self.game_board)

        # ensuring the stack is in the order it should be in
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)

        # test if the turite is occupied by a Landmine object and not the avatar
        self.assertTrue(isinstance(self.turite_station.occupied_by, Landmine))
        self.assertNotEqual(self.turite_station.occupied_by, self.client.avatar)

        # test if Dynamite is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_landmine: Landmine = self.turite_station.occupied_by  # returns the correct type; ignore warning
        self.assertEqual(placed_landmine.occupied_by, self.client.avatar)

        self.assertEqual(self.avatar.place_trap.cooldown, 1)  # double-check the ability cooldown reset

    def test_placing_emp(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # ensuring the stack is in the order it should be in
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)

        # test if the turite is occupied by an EMP object and not the avatar
        self.assertTrue(isinstance(self.turite_station.occupied_by, EMP))
        self.assertNotEqual(self.turite_station.occupied_by, self.client.avatar)

        # test if EMP is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_emp: EMP = self.turite_station.occupied_by  # returns the correct type; ignore warning
        self.assertEqual(placed_emp.occupied_by, self.client.avatar)

        self.assertEqual(self.avatar.place_trap.cooldown, 1)  # double-check the ability cooldown reset

    def test_placing_multiple_dynamite(self):
        self.test_placing_dynamite()  # call previous test to set up test
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.client, self.game_board)

        # needed stack order: Copium -> Lambdium -> Turite -> Dynamite -> Avatar
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)
        self.assertTrue(isinstance(self.turite_station.occupied_by, Dynamite))
        self.assertEqual(self.turite_station.occupied_by.occupied_by, self.avatar)

    def test_placing_multiple_landmines(self):
        self.test_placing_landmine()  # call previous test to set up test
        self.place_controller.handle_actions(ActionType.PLACE_LANDMINE, self.client, self.game_board)

        # needed stack order: Copium -> Lambdium -> Turite -> Landmine -> Avatar
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)
        self.assertTrue(isinstance(self.turite_station.occupied_by, Landmine))
        self.assertEqual(self.turite_station.occupied_by.occupied_by, self.avatar)

    def test_placing_multiple_emps(self):
        self.test_placing_emp()  # call previous test to set up test
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # needed stack order: Copium -> Lambdium -> Turite -> Landmine -> Avatar
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)
        self.assertTrue(isinstance(self.turite_station.occupied_by, EMP))
        self.assertEqual(self.turite_station.occupied_by.occupied_by, self.avatar)

    def test_placing_multiple_dynamite_and_traps(self):
        self.test_placing_dynamite()  # call previous test to set up test

        # try to place duplicate dynamite
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.client, self.game_board)

        # place first emp
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # allow the avatar to place next EMP by making the fuse 0
        self.avatar.place_trap.fuse = 0

        # try to place duplicate emp
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # needed stack order: Copium -> Lambdium -> Turite -> Dynamite -> EMP -> Avatar
        self.assertEqual(self.copium_station.occupied_by, self.lambdium_station)
        self.assertEqual(self.lambdium_station.occupied_by, self.turite_station)
        self.assertTrue(isinstance(self.turite_station.occupied_by, Dynamite))
        self.assertTrue(isinstance(self.turite_station.occupied_by.occupied_by, EMP))
        self.assertEqual(self.turite_station.occupied_by.occupied_by.occupied_by, self.avatar)
