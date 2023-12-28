from __future__ import annotations

from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.player import Player
from game.controllers.controller import Controller
from game.controllers.interact_controller import InteractController
from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation


class MineController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard) -> None:
        """
        If the given enum is for mining, all adjacent tiles will be checked for the ore wanted. If not found, None
        will be returned.

        For example, if the ActionType is MINE_COPIUM, the adjacent tiles will be checked. The first instance of copium
        will be taken, and it stops there. If no copium is found, None will be returned.
        """

        # don't mine anything if the inventory is full
        if len(world.inventory_manager.get_inventory(client.avatar.company)) == 50:
            return

        match action:
            case ActionType.MINE:
                client.avatar.state = 'mining'
                InteractController().handle_actions(ActionType.INTERACT_CENTER, client, world)
                tile: Tile = world.game_map[client.avatar.position.y][client.avatar.position.x]
                station: OreOccupiableStation = tile.occupied_by  # Will return the OreOccupiableStation if it isn't

                if station is None:
                    return

                # remove the OreOccupiableStation from the game board
                station.remove_from_game_board(tile)
            case _:  # default case
                return
