import unittest

from game.common.avatar import Avatar
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
        self.ore_station: OreOccupiableStation = OreOccupiableStation()

        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1),): [self.ore_station],
            (Vector(1, 0),): [self.avatar]
        }

        self.game_board = GameBoard(0, Vector(3, 3), self.locations, False)

        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

        # Unlock the entire tech tree up to landmines for testing
        self.avatar.buy_new_tech('Better Drivetrains')
        self.avatar.buy_new_tech('Unnamed Drivetrain Tech')
        self.avatar.buy_new_tech('Overdrive Movement')
        self.avatar.buy_new_tech('High Yield Mining')
        self.avatar.buy_new_tech('Unnamed Mining Tech')
        self.avatar.buy_new_tech('Dynamite')
        self.avatar.buy_new_tech('Landmines')

    # tests that the avatar is at the top of the stack
    def test_avatar_on_top_of_ore_station(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)  # move to position
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 1)))  # ensure position is fine
        self.assertEqual(self.ore_station.occupied_by, self.client.avatar)  # ensure avatar is on top

    def test_placing_dynamite(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.client, self.game_board)

        # show the ore station's first occupied_by is a Dynamite object and not the avatar
        self.assertTrue(isinstance(self.ore_station.occupied_by, Dynamite))
        self.assertNotEqual(self.ore_station.occupied_by, self.client.avatar)

        # test if Dynamite is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_dyn: Dynamite = self.ore_station.occupied_by  # returns the correct type; ignore warning
        self.assertEqual(placed_dyn.occupied_by, self.client.avatar)

        # double-check the ability cooldown reset
        self.assertEqual(self.avatar.dynamite_active_ability.cooldown, 1)

    def test_placing_landmine(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_LANDMINE, self.client, self.game_board)

        # show the ore station's first occupied_by is a Landmine object and not the avatar
        self.assertTrue(isinstance(self.ore_station.occupied_by, Landmine))
        self.assertNotEqual(self.ore_station.occupied_by, self.client.avatar)

        # test if Landmine is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_landmine: Landmine = self.ore_station.occupied_by  # returns the correct type; ignore warning
        self.assertEqual(placed_landmine.occupied_by, self.client.avatar)

        # double-check the ability cooldown reset
        self.assertEqual(self.avatar.landmine_active_ability.cooldown, 1)

    def test_placing_emp(self) -> None:
        self.avatar.buy_new_tech('EMPs')  # unlock emps for testing

        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # show the ore station's first occupied_by is an EMP object and not the avatar
        self.assertTrue(isinstance(self.ore_station.occupied_by, EMP))
        self.assertNotEqual(self.ore_station.occupied_by, self.client.avatar)

        # test if EMP is occupied by the Avatar (i.e., Avatar at the top of the stack)
        placed_emp: EMP = self.ore_station.occupied_by  # returns the correct type; ignore warning
        self.assertEqual(placed_emp.occupied_by, self.client.avatar)

        self.assertEqual(self.avatar.emp_active_ability.cooldown, 1)  # double-check the ability cooldown reset

    # test that 2 dynamite aren't on the same tile
    def test_placing_multiple_dynamite(self):
        self.test_placing_dynamite()  # call previous test to set up test
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.client, self.game_board)

        # show that the avatar can't place dynamite due to cooldown
        self.assertFalse(self.avatar.dynamite_active_ability.is_usable)

        # set fuse to 0 so that active ability is usable
        self.avatar.dynamite_active_ability.fuse = 0
        self.assertTrue(self.avatar.can_place_dynamite())

        # attempt to place dynamite down
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.client, self.game_board)

        # needed stack order: OreOccupiableStation -> Dynamite -> Avatar
        self.assertTrue(isinstance(self.ore_station.occupied_by, Dynamite))
        self.assertEqual(self.ore_station.occupied_by.occupied_by, self.avatar)

    def test_placing_multiple_landmines(self):
        self.test_placing_landmine()  # call previous test to set up test
        self.place_controller.handle_actions(ActionType.PLACE_LANDMINE, self.client, self.game_board)

        # show that the avatar can't place a landmine due to cooldown
        self.assertFalse(self.avatar.landmine_active_ability.is_usable)

        # set fuse to 0 so that active ability is usable
        self.avatar.landmine_active_ability.fuse = 0
        self.assertTrue(self.avatar.can_place_landmine())

        # attempt to place landmine down
        self.place_controller.handle_actions(ActionType.PLACE_LANDMINE, self.client, self.game_board)

        # needed stack order: OreOccupiableStation -> Landmine -> Avatar
        self.assertTrue(isinstance(self.ore_station.occupied_by, Landmine))
        self.assertEqual(self.ore_station.occupied_by.occupied_by, self.avatar)

    def test_placing_multiple_emps(self):
        self.test_placing_emp()  # call previous test to set up test
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # show that the avatar can't place EMP due to cooldown
        self.assertFalse(self.avatar.emp_active_ability.is_usable)

        # set fuse to 0 so that active ability is usable
        self.avatar.emp_active_ability.fuse = 0
        self.assertTrue(self.avatar.can_place_emp())

        # attempt to place an EMP down
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # needed stack order: OreOccupiableStation -> EMP -> Avatar
        self.assertTrue(isinstance(self.ore_station.occupied_by, EMP))
        self.assertEqual(self.ore_station.occupied_by.occupied_by, self.avatar)

    def test_placing_multiple_dynamite_and_traps(self):
        self.avatar.buy_new_tech('EMPs')  # unlock emps for testing
        self.test_placing_dynamite()  # call previous test to set up test

        # try to place duplicate dynamite
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.client, self.game_board)

        # place first emp
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # allow the avatar to place next EMP by making the fuse 0
        self.avatar.emp_active_ability.fuse = 0
        self.assertTrue(self.avatar.can_place_emp())

        # try to place duplicate emp
        self.place_controller.handle_actions(ActionType.PLACE_EMP, self.client, self.game_board)

        # needed stack order: OreOccupiableStation -> Dynamite -> EMP -> Avatar
        self.assertTrue(isinstance(self.ore_station.occupied_by, Dynamite))
        self.assertTrue(isinstance(self.ore_station.occupied_by.occupied_by, EMP))
        self.assertEqual(self.ore_station.occupied_by.occupied_by.occupied_by, self.avatar)
