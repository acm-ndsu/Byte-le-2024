from __future__ import annotations

from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller
from game.controllers.interact_controller import InteractController


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

        InteractController().handle_actions(ActionType.INTERACT_CENTER, client, world, ore_object_type)

        world.game_map[client.avatar.position.y][client.avatar.position.x].remove_from_occupied_by(ore_object_type)
