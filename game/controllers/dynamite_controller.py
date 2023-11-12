from __future__ import annotations

from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.stations.station import Station
from game.controllers.controller import Controller
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.utils.vector import Vector


class DynamiteController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_detonation(self, dynamite: Dynamite, world: GameBoard) -> None:
        """
        By taking a dynamite object, its adjacent tiles and the one is on will be collected. Then, the dynamite will
        explode and collect the first ore or ancient tech it finds.
        """

        # don't do anything if the dynamite can't explode
        if not dynamite.is_fuse_at_0():
            return

        adjacent_tiles: list[Vector] = [dynamite.position,
                                        Vector.add_vectors(dynamite.position, Vector(0, -1)),  # up tile
                                        Vector.add_vectors(dynamite.position, Vector(1, 0)),  # right tile
                                        Vector.add_vectors(dynamite.position, Vector(0, 1)),  # down tile
                                        Vector.add_vectors(dynamite.position, Vector(-1, 0))]  # left tile

        # reference variable for later; will either be None or a Station subclass
        station: Station | None = None

        for vector in adjacent_tiles:
            tile: Tile = world.game_map[vector.y][vector.x]

            if tile.is_occupied_by_object_type(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION):
                station = tile.remove_from_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION)
            elif tile.is_occupied_by_object_type(self.__wanted_ore(dynamite.company)):
                station = tile.remove_from_occupied_by(self.__wanted_ore(dynamite.company))
            elif tile.is_occupied_by_object_type(ObjectType.COPIUM_OCCUPIABLE_STATION):
                station = tile.remove_from_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION)
            elif tile.is_occupied_by_object_type(self.__not_wanted_ore(dynamite.company)):
                station = tile.remove_from_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION)

            if station is not None:
                world.inventory_manager.give(station.held_item, dynamite.company)

    # helper method that returns the object_type of the players preferred ore for their company
    def __wanted_ore(self, company: Company) -> ObjectType:
        return ObjectType.LAMBDIUM_OCCUPIABLE_STATION if company is Company.CHURCH \
            else ObjectType.TURITE_OCCUPIABLE_STATION

    # helper method that returns the object_type of the opposing team's ore
    def __not_wanted_ore(self, company: Company) -> ObjectType:
        return ObjectType.LAMBDIUM_OCCUPIABLE_STATION if company is Company.TURING \
            else ObjectType.TURITE_OCCUPIABLE_STATION