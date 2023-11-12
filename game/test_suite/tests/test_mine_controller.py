import unittest

from game.common.enums import Company
from game.common.map.game_board import GameBoard
from game.controllers.mine_controller import MineController
from game.controllers.movement_controller import MovementController
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
        self.movement_controller = MovementController()
        self.avatar = Avatar(position=Vector(1, 1), company=Company.CHURCH)

        # adds ores to all adjacent tiles and the one the avatar will be on
        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1), Vector(1, 1)): [AncientTechOccupiableStation(), self.avatar],
            (Vector(1, 0),): [LambdiumOccupiableStation(), CopiumOccupiableStation()],
            (Vector(2, 1),): [CopiumOccupiableStation(), LambdiumOccupiableStation(),
                              TuriteOccupiableStation()],
            (Vector(0, 1),): [CopiumOccupiableStation()],
            (Vector(1, 2),): [TuriteOccupiableStation(), LambdiumOccupiableStation()]
        }

        self.world: GameBoard = GameBoard(0, Vector(3, 3), self.locations, False)
        self.client: Player = Player(avatar=self.avatar)
        self.world.generate_map()

    # tests getting the material from underneath the avatar
    def test_mining(self):
        # remember that the game map is **(y, x)**, not (x, y)
        self.mine_controller.handle_actions(ActionType.MINE_ANCIENT_TECH, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   AncientTech))

        # ensure all tiles are the same except the center
        self.assertTrue(self.world.game_map[1][1].is_occupied_by_object_type(ObjectType.AVATAR) and not
        self.world.game_map[1][1].is_occupied_by_object_type(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION))

    def test_mining_fail(self):
        self.mine_controller.handle_actions(ActionType.MINE_ANCIENT_TECH, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_ANCIENT_TECH, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   AncientTech))
        self.assertTrue(self.world.inventory_manager.get_inventory(self.avatar.company)[1] is None)

    def test_mining_lambdium(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_LAMBUIM, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   Lambdium))

    def test_mining_copium(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_COPIUM, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   Copium))

    def test_mining_turite(self):
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_TURITE, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
                                   Turite))

    def test_mining_until_empty(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_TURITE, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_COPIUM, self.client, self.world)
        self.mine_controller.handle_actions(ActionType.MINE_LAMBUIM, self.client, self.world)
        [isinstance(x[0], x[1]) for x in zip(self.world.inventory_manager.get_inventory(self.avatar.company)[:2],
                                             (Turite, Copium, Lambdium))]
