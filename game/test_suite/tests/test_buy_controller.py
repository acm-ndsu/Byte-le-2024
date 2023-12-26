import unittest

from game.common.enums import Company
from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.controllers.buy_tech_controller import BuyTechController
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.quarry_rush.station.company_station import ChurchStation, TuringStation
from game.utils.vector import Vector
from game.common.player import Player
from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject


class TestBuyController(unittest.TestCase):
    """
    A class to test buying all techs.
    """

    def setUp(self):
        self.movement_controller = MovementController()
        self.buy_tech_controller = BuyTechController()
        self.avatar: Avatar = Avatar(position=Vector(0, 0), company=Company.TURING)
        self.avatar.science_points = 10000  # set science points to unlock techs

        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(0, 0),): [ChurchStation()],  # top left
            (Vector(0, 0),): [self.avatar],
            (Vector(1, 0),): [TuringStation()],  # top right
        }

        # make a 2x2 game map
        self.world = GameBoard(0, Vector(4, 4), self.locations, False)
        self.client = Player(None, None, [], self.avatar)
        self.world.generate_map()

    # test that buying a tech when not on your home base doesn't work
    def test_not_on_home_base(self):
        self.buy_tech_controller.handle_actions(ActionType.BUY_IMPROVED_MINING, self.client, self.world)

        # will be a size of 1 due to default tech provided in tech tree
        self.assertTrue(len(self.client.avatar.get_researched_techs()) == 1)

    def test_on_random_tile(self):
        # move to a tile with nothing on it and try to buy a tech; result shouldn't change from above
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.world)
        self.test_not_on_home_base()

    # test buying a tech with 0 science points
    def test_buying_no_science_points(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.world)
        self.avatar.science_points = 0

        # will be a size of 1 due to default tech provided in tech tree
        self.assertTrue(len(self.client.avatar.get_researched_techs()) == 1)

    # test that buying all techs works; taking emp route
    def test_buying_all_techs(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.world)

        self.buy_tech_controller.handle_actions(ActionType.BUY_IMPROVED_DRIVETRAIN, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_SUPERIOR_DRIVETRAIN, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_OVERDRIVE_DRIVETRAIN, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_IMPROVED_MINING, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_SUPERIOR_MINING, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_OVERDRIVE_MINING, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_DYNAMITE, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_LANDMINES, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_EMPS, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_TRAP_DEFUSAL, self.client, self.world)

        # check final size of researched techs
        self.assertTrue(len(self.client.avatar.get_researched_techs()) == 10)

    # test that you can't buy a tech you didn't build up to in the tech tree
    def test_buying_tech_out_of_order(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.world)

        self.buy_tech_controller.handle_actions(ActionType.BUY_SUPERIOR_DRIVETRAIN, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_DYNAMITE, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_EMPS, self.client, self.world)
        self.buy_tech_controller.handle_actions(ActionType.BUY_TRAP_DEFUSAL, self.client, self.world)

        # check final size of researched techs
        self.assertTrue(len(self.client.avatar.get_researched_techs()) == 1)