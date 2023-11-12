import unittest

from game.common.action import ActionType
from game.common.enums import Company
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.dynamite_controller import DynamiteController
from game.controllers.place_controller import PlaceController
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.station.ancient_tech_occupiable_station import AncientTechOccupiableStation
from game.quarry_rush.station.ore_occupiable_stations import *
from game.utils.vector import Vector


class TestDynamiteController(unittest.TestCase):
    """
    Tests the Dynamite Controller
    """

    def setUp(self) -> None:
        self.dynamite_controller: DynamiteController = DynamiteController()
        self.place_controller: PlaceController = PlaceController()

        self.avatar = Avatar(position=Vector(1, 1), company=Company.CHURCH)
        self.player: Player = Player(avatar=self.avatar)

        # adds ores to all adjacent tiles and the one the avatar will be on
        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1), Vector(1, 1)): [AncientTechOccupiableStation(), self.avatar],  # center tile
            (Vector(1, 0),): [CopiumOccupiableStation(), LambdiumOccupiableStation()],  # up tile
            (Vector(2, 1),): [CopiumOccupiableStation(), TuriteOccupiableStation()],  # right tile
            (Vector(1, 2),): [TuriteOccupiableStation()],  # down tile

            # left tile
            (Vector(0, 1),): [CopiumOccupiableStation(), LambdiumOccupiableStation(), TuriteOccupiableStation()]
        }

        self.world: GameBoard = GameBoard(0, Vector(3, 3), self.locations, False)
        self.client: Player = Player(avatar=self.avatar)
        self.world.generate_map()

    def test_no_explosion(self):
        # make sure the dynamite is placed properly
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.player, self.world)
        self.assertTrue(self.world.game_map[self.avatar.position.y][self.avatar.position.x].is_occupied_by_object_type(
            ObjectType.DYNAMITE))

        dynamite: Dynamite = self.world.game_map[self.avatar.position.y][self.avatar.position.x].get_occupied_by(
            ObjectType.DYNAMITE)

        # the dynamite cannot explode yet because the tick isn't 0
        self.assertFalse(dynamite.can_explode)

    def test_explosion(self):
        # make sure the dynamite is placed properly
        self.place_controller.handle_actions(ActionType.PLACE_DYNAMITE, self.player, self.world)
        self.assertTrue(self.world.game_map[self.avatar.position.y][self.avatar.position.x].is_occupied_by_object_type(
            ObjectType.DYNAMITE))

        dynamite: Dynamite = self.world.game_map[self.avatar.position.y][self.avatar.position.x].get_occupied_by(
            ObjectType.DYNAMITE)

        # the dynamite cannot explode yet because the tick isn't 0
        self.assertFalse(dynamite.can_explode)

        dynamite.decrement_fuse()

        # dynamite can now explode
        self.assertTrue(dynamite.can_explode)

        # should add ores in the order: AncientTech -> Lambdium -> Copium -> Turite -> Lambium
        self.dynamite_controller.handle_detonation(dynamite, self.world)

        # inventory size should be 5, and check the order of the list is correct
        self.assertTrue(len(self.world.inventory_manager.get_inventory(self.avatar.company)), 5)
        self.assertEquals(self.world.inventory_manager.get_inventory(self.avatar.company)[0].object_type,
                          ObjectType.ANCIENT_TECH)  # from center tile
        self.assertEquals(self.world.inventory_manager.get_inventory(self.avatar.company)[1].object_type,
                          ObjectType.LAMBDIUM)  # from up tile
        self.assertEquals(self.world.inventory_manager.get_inventory(self.avatar.company)[2].object_type,
                          ObjectType.COPIUM)  # from right tile
        self.assertEquals(self.world.inventory_manager.get_inventory(self.avatar.company)[3].object_type,
                          ObjectType.TURITE)  # from down tile
        self.assertEquals(self.world.inventory_manager.get_inventory(self.avatar.company)[4].object_type,
                          ObjectType.LAMBDIUM)  # from left tile

        # ensure the tiles still contain the rest of the stations

        # the center tile should still have the dynamite object on it; gameboard will remove it
        self.assertTrue(self.world.game_map[1][1].is_occupied_by_object_type(ObjectType.DYNAMITE) and
                        self.world.game_map[1][1].is_occupied_by_object_type(ObjectType.AVATAR))
        self.assertTrue(self.world.game_map[0][1].is_occupied_by_object_type(ObjectType.COPIUM_OCCUPIABLE_STATION))  # up tile
        self.assertTrue(self.world.game_map[1][2].is_occupied_by_object_type(ObjectType.TURITE_OCCUPIABLE_STATION))  # right tile
        self.assertTrue(self.world.game_map[2][1].occupied_by is None)  # down tile
        self.assertTrue(self.world.game_map[1][0].is_occupied_by_object_type(ObjectType.COPIUM_OCCUPIABLE_STATION) and  # left tile
                        self.world.game_map[1][0].is_occupied_by_object_type(ObjectType.TURITE_OCCUPIABLE_STATION))
