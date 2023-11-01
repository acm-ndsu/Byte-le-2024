from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.player import Player
from game.controllers.controller import Controller
from game.quarry_rush.entity.ores import Ore
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.traps import Landmine, EMP, Trap
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

        # add all adjacent tiles to a list
        adjacent_tiles: [Tile] = [Vector.add_vectors(avatar_pos, Vector(0, 1)),
                                  Vector.add_vectors(avatar_pos, Vector(0, -1)),
                                  Vector.add_vectors(avatar_pos, Vector(1, 0)),
                                  Vector.add_vectors(avatar_pos, Vector(-1, 0))]

        ore: Ore
        # match action:
        #     case ActionType.MINE_COPIUM:
        #
        #     case ActionType.MINE_TURITE:
        #         pass
        #     case ActionType.MINE_LAMBUIM:
        #         pass
        #     case ActionType.MINE_ANCIENT_TECH:
        #         pass

    # def find_ore(self, tiles: [Tile]):
    #     for tile in tiles:
    #         if tile.

