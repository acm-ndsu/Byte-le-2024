from __future__ import annotations

from game.common.avatar import Avatar
from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.player import Player
from game.controllers.controller import Controller
from game.controllers.interact_controller import InteractController
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.utils.vector import Vector


class DynamiteController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_detonation(self, dynamite: Dynamite, client: Player, world: GameBoard) -> None:
        """
        By taking a dynamite object, its adjacent tiles and the one is on will be collected. Then, the dynamite will
        explode and collect the first ore or ancient tech it finds.
        """
        avatar: Avatar = client.avatar

        adjacent_tiles: list[Tile | None] = [dynamite.position,
                                             Vector.add_vectors(dynamite.position, Vector(0, -1)),  # up tile
                                             Vector.add_vectors(dynamite.position, Vector(1, 0)),  # right tile
                                             Vector.add_vectors(dynamite.position, Vector(0, -1)),  # down tile
                                             Vector.add_vectors(dynamite.position, Vector(-1, 0))]  # left tile

        # instantiates an interact controller because it has a check to mine from a tile
        interact_controller: InteractController = InteractController()
        for tile in adjacent_tiles:
            if tile.is_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION):
                pass
