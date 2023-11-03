import unittest

from game.common.enums import Company
from game.common.map.game_board import GameBoard
from game.controllers.mine_controller import MineController
from game.quarry_rush.entity.ancient_tech import AncientTech
from game.quarry_rush.station.ore_occupiable_stations import *
from game.quarry_rush.station.ancient_tech_occupiable_station import AncientTechOccupiableStation
from game.utils.vector import Vector
from game.common.player import Player
from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject


class TestMineController(unittest.TestCase):
    """
    Tests the MineController.
    """

    def setUp(self) -> None:
        self.mine_controller: MineController = MineController()
        self.avatar = Avatar(position=Vector(1, 1), company=Company.CHURCH)

        # adds ores to all adjacent tiles and the one the avatar will be on
        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1), Vector(1, 1)): [AncientTechOccupiableStation(), self.avatar],
            (Vector(1, 0), Vector(1, 0)): [LambdiumOccupiableStation(), CopiumOccupiableStation()],
            (Vector(2, 1), Vector(2, 1), Vector(2, 1)): [CopiumOccupiableStation(), LambdiumOccupiableStation(),
                                                         TuriteOccupiableStation()],
            (Vector(0, 1), Vector(0, 1)): [CopiumOccupiableStation()],
            (Vector(1, 2), Vector(1, 2)): [TuriteOccupiableStation(), LambdiumOccupiableStation()]
        }

        self.world: GameBoard = GameBoard(0, Vector(3, 3), self.locations, False)
        self.client: Player = Player(None, None, [], self.avatar)
        self.world.generate_map()

    # tests getting the material from underneath the avatar
    def test_mining_center(self):
        # remember that the game map is **(y, x)**, not (x, y)
        self.mine_controller.handle_actions(ActionType.MINE_ANCIENT_TECH, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   AncientTech))

        # ensure all tiles are the same except the center
        self.assertTrue(self.world.game_map[1][1].is_occupied_by(ObjectType.AVATAR) and not
                        self.world.game_map[1][1].is_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[0][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[0][1].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][2].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][0].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[2][1].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION) and
                        self.world.game_map[2][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))

    # tests mining above the avatar
    def test_mining_above(self):
        self.mine_controller.handle_actions(ActionType.MINE_LAMBUIM, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   Lambdium))

        self.assertTrue(self.world.game_map[1][1].is_occupied_by(ObjectType.AVATAR) and
                        self.world.game_map[1][1].is_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[0][1].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and not
                        self.world.game_map[0][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][2].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][0].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[2][1].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION) and
                        self.world.game_map[2][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))

    # tests mining to the right of the avatar
    def test_mining_right(self):
        self.mine_controller.handle_actions(ActionType.MINE_TURITE, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   Turite))

        self.assertTrue(self.world.game_map[1][1].is_occupied_by(ObjectType.AVATAR) and
                        self.world.game_map[1][1].is_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[0][1].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[0][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][2].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and not
                        self.world.game_map[1][2].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][0].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[2][1].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION) and
                        self.world.game_map[2][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))

    # tests mining for the same ore twice to get it successfully
    def test_mining_twice(self):
        self.mine_controller.handle_actions(ActionType.MINE_TURITE, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_TURITE, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   Turite),
                        isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[1], Turite))

        self.assertTrue(self.world.game_map[1][1].is_occupied_by(ObjectType.AVATAR) and
                        self.world.game_map[1][1].is_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[0][1].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[0][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][2].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and not
                        self.world.game_map[1][2].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][0].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[2][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and not
                        self.world.game_map[2][1].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))

    # tests mining for the same ore 3 times to get it successfully
    def test_mining_three_times(self):
        self.mine_controller.handle_actions(ActionType.MINE_COPIUM, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_COPIUM, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_COPIUM, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   Copium) and
                        isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[1],
                                   Copium) and
                        isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[2],
                                   Copium))

        self.assertTrue(self.world.game_map[1][1].is_occupied_by(ObjectType.AVATAR) and
                        self.world.game_map[1][1].is_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION))

        self.assertTrue(not self.world.game_map[0][1].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[0][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][2].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION) and not
                        self.world.game_map[1][2].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(not self.world.game_map[1][0].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[2][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[2][1].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))

    def test_mining_with_none(self):
        self.mine_controller.handle_actions(ActionType.MINE_ANCIENT_TECH, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_ANCIENT_TECH, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   AncientTech) and
                        self.world.inventory_manager.get_inventory(self.avatar.company)[1] is None)

        self.assertTrue(self.world.game_map[1][1].is_occupied_by(ObjectType.AVATAR) and not
        self.world.game_map[1][1].is_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[0][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[0][1].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][2].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION) and
                        self.world.game_map[1][2].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[1][0].is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        self.assertTrue(self.world.game_map[2][1].is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION) and
                        self.world.game_map[2][1].is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))
