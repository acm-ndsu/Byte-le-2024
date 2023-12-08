from __future__ import annotations

from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.controllers.controller import Controller
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation
from game.utils.vector import Vector


class DynamiteController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_detonation(self, dynamite: Dynamite, world: GameBoard) -> None:
        """
        By taking a dynamite object, its adjacent tiles and the one it's on will be collected. Then, the dynamite will
        explode and add the held items from the stations to the given avatar.
        """

        # don't do anything if the dynamite can't explode
        if not dynamite.is_fuse_at_0():
            return

        adjacent_tiles: list[Vector] = [dynamite.position,
                                        Vector.add_vectors(dynamite.position, Vector(0, -1)),  # up tile
                                        Vector.add_vectors(dynamite.position, Vector(1, 0)),  # right tile
                                        Vector.add_vectors(dynamite.position, Vector(0, 1)),  # down tile
                                        Vector.add_vectors(dynamite.position, Vector(-1, 0))]  # left tile

        # reference variable for later; will either be None or an OreOccupiableStation subclass
        station: OreOccupiableStation | None = None

        for vector in adjacent_tiles:
            tile: Tile = world.game_map[vector.y][vector.x]

            # don't do anything if the occupied_by isn't an OreOccupiableStation
            if not isinstance(tile.occupied_by, OreOccupiableStation):
                return

            # call the give_item method to give the station's item to the dynamite's owner
            station = tile.occupied_by
            station.give_item(dynamite.company, world.inventory_manager)

            # remove the station from the gameboard if it doesn't have a held item
            station.remove_from_game_board(tile)
