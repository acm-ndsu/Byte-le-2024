from game.common.game_object import GameObject
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.enums import *
from game.quarry_rush.station.company_station import CompanyStation
from game.utils.vector import Vector
from game.controllers.controller import Controller


class BuyTechController(Controller):
    """
    This controller simplifies buying techs by letting players pass in an ActionType enum representing the
    tech they want to buy. It will check if the client's avatar is first on their respective base. If so,
    it will call the methods needed to purchase the desired tech.
    """
    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        if not self.__is_on_home_base(client, world):  # escapes method if not on home base
            return

        tech_name: str = ''

        match action:
            case ActionType.BUY_IMPROVED_DRIVETRAIN:
                tech_name = 'Improved Drivetrain'
            case ActionType.BUY_SUPERIOR_DRIVETRAIN:
                tech_name = 'Superior Drivetrain'
            case ActionType.BUY_OVERDRIVE_DRIVETRAIN:
                tech_name = 'Overdrive Drivetrain'
            case ActionType.BUY_IMPROVED_MINING:
                tech_name = 'Improved Mining'
            case ActionType.BUY_SUPERIOR_MINING:
                tech_name = 'Superior Mining'
            case ActionType.BUY_OVERDRIVE_MINING:
                tech_name = 'Overdrive Mining'
            case ActionType.BUY_DYNAMITE:
                tech_name = 'Dynamite'
            case ActionType.BUY_LANDMINES:
                tech_name = 'Landmines'
            case ActionType.BUY_EMPS:
                tech_name = 'EMPs'
            case ActionType.BUY_TRAP_DEFUSAL:
                tech_name = 'Trap Defusal'

        client.avatar.buy_new_tech(tech_name)  # buy the tech specified

    def __is_on_home_base(self, client: Player, world: GameBoard):
        avatar_pos: Vector = client.avatar.position  # get the position of the avatar
        tile: Tile = world.game_map[avatar_pos.y][avatar_pos.x]  # get the tile the avatar is on

        if not isinstance(tile.occupied_by, CompanyStation):  # if not a CompanyStation, immediately return False
            return False

        station: CompanyStation = tile.occupied_by  # confirmed station is a CompanyStation from if statement

        return station.company == client.avatar.company  # return if the companies match
