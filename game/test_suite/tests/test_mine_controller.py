import unittest

from unittest.mock import Mock
from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.mine_controller import MineController
from game.controllers.movement_controller import MovementController
from game.quarry_rush.station.ore_occupiable_station import *
from game.utils.vector import Vector


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
            (Vector(1, 1), Vector(1, 1)): [OreOccupiableStation(), self.avatar]
        }

        self.world: GameBoard = GameBoard(0, Vector(3, 3), self.locations, False)
        self.client: Player = Player(avatar=self.avatar)
        self.world.generate_map()

    # tests getting the material from underneath the avatar
    def test_mining(self):
        self.mine_controller.handle_actions(ActionType.MINE, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0], Copium))

        # remember that the game map is **(y, x)**, not (x, y)
        # self.mine_controller.handle_actions(ActionType.MINE, self.client, self.world)
        # print(f'Inventory: {self.world.inventory_manager.get_inventory(self.avatar.company)[0]}')
        # self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
        #                            Copium))

    # test mining with a drop rate higher than one
    def test_mining_high_drop_rate(self):
        self.client.avatar.drop_rate = 3
        self.mine_controller.handle_actions(ActionType.MINE, self.client, self.world)
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0], Copium))
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[1], Copium))
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[2], Copium))

    # make sure that after mining with a high drop rate, the points gained are correct
    def test_points_gained_high_drop_rate(self):
        self.test_mining_high_drop_rate()
        self.assertEqual(self.world.inventory_manager.cash_in_points(Company.CHURCH), 30)  # 1 copium = 10 pts
    def test_mining_full_inventory(self):
        # fill inventory
        [self.world.inventory_manager.give(Turite(), self.client.avatar.company) for x in range(50)]

        # attempt to mine
        self.mine_controller.handle_actions(ActionType.MINE, self.client, self.world)

        # ensure the last slot is still Turite and not Copium
        self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.client.avatar.company)[49],
                                   Turite))

    # def test_mining_fail(self):
    #     pass
        # self.mine_controller.handle_actions(ActionType.MINE_ANCIENT_TECH, self.client, self.world)
        # self.mine_controller.handle_actions(ActionType.MINE_ANCIENT_TECH, self.client, self.world)
        # self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
        #                            AncientTech))
        # self.assertTrue(self.world.inventory_manager.get_inventory(self.avatar.company)[1] is None)

    # def test_mining_lambdium(self):
    #     station: OreOccupiableStation = self.locations[(Vector(1, 1), Vector(1, 1))][0]
    #     station.rand.random = lambda : 0.05
    #     self.mine_controller.handle_actions(ActionType.MINE, self.client, self.world)
    #     self.mine_controller.handle_actions(ActionType.MINE, self.client, self.world)
    #
    #     self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
    #                                Copium))
    #     self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[1],
    #                                Lambdium))


    # def test_mining_copium(self):
        # self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.world)
        # self.mine_controller.handle_actions(ActionType.MINE_COPIUM, self.client, self.world)
        # self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
        #                            Copium))

    # def test_mining_turite(self):
        # self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.world)
        # self.mine_controller.handle_actions(ActionType.MINE_TURITE, self.client, self.world)
        # self.assertTrue(isinstance(self.world.inventory_manager.get_inventory(self.avatar.company)[0],
        #                            Turite))

    # def test_mining_until_empty(self):
    #     self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.world)
    #     self.mine_controller.handle_actions(ActionType.MINE_TURITE, self.client, self.world)
    #     self.mine_controller.handle_actions(ActionType.MINE_COPIUM, self.client, self.world)
    #     self.mine_controller.handle_actions(ActionType.MINE_LAMBUIM, self.client, self.world)
    #     [isinstance(x[0], x[1]) for x in zip(self.world.inventory_manager.get_inventory(self.avatar.company)[:2],
    #                                          (Turite, Copium, Lambdium))]
