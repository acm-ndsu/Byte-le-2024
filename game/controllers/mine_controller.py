from __future__ import annotations

from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.player import Player
from game.controllers.controller import Controller
from game.quarry_rush.entity.ores import Ore
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.traps import Landmine, EMP, Trap
from game.quarry_rush.station.ore_occupiable_stations import OreOccupiableStation
from game.utils.vector import Vector


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

        avatar_pos: Vector = client.avatar.position

        # add all adjacent and central tiles to a list in clockwise motion
        adjacent_tiles: [Tile] = [world.game_map[avatar_pos.y][avatar_pos.x],  # center tile
                                  world.game_map[avatar_pos.y - 1][avatar_pos.x],  # above tile
                                  world.game_map[avatar_pos.y][avatar_pos.x + 1],  # right tile
                                  world.game_map[avatar_pos.y + 1][avatar_pos.x],  # below tile
                                  world.game_map[avatar_pos.y][avatar_pos.x - 1]]  # left tile

        ore_object_type: ObjectType

        match action:
            case ActionType.MINE_COPIUM:
                ore_object_type = ObjectType.COPIUM_OCCUPIABLE_STATION
            case ActionType.MINE_TURITE:
                ore_object_type = ObjectType.TURITE_OCCUPIABLE_STATION
            case ActionType.MINE_LAMBUIM:
                ore_object_type = ObjectType.LAMBDIUM_OCCUPIABLE_STATION
            case ActionType.MINE_ANCIENT_TECH:
                ore_object_type = ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION
            case _:  # default case
                return

        ore: Ore | None = None
        for tile in adjacent_tiles:
            if tile.is_occupied_by(ore_object_type):
                ore_station: OreOccupiableStation = tile.remove_from_occupied_by(ore_object_type)
                ore = ore_station.held_item  # found ore wanted
                break

        # gives the ore to the player's inventory
        world.inventory_manager.give(ore, client.avatar.company)
