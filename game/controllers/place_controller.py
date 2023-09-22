from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.enums import *
from game.controllers.controller import Controller
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.trap import *
from game.quarry_rush.avatar.inventory_manager import InventoryManager


class PlaceController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        avatar_pos: Vector = client.avatar.position
        tile: Tile = world.game_map[avatar_pos.x][avatar_pos.y]

        # depending on the action type, the type of placeable entity is placed on the map with the avatar occupying it
        match action:
            case ActionType.PLACE_DYNAMITE:
                if client.avatar.can_place_dynamite():
                    dynamite: Dynamite = Dynamite()
                    dynamite.occupied_by = client.avatar
                    tile.occupied_by = dynamite
            case ActionType.PLACE_LANDMINE:
                if client.avatar.can_place_trap():
                    landmine: Landmine = Landmine()  # need to figure out constructor
                    landmine.occupied_by = client.avatar
                    tile.occupied_by = landmine
            case ActionType.PLACE_EMP:
                if client.avatar.can_place_trap():
                    emp: EMP = EMP()  # need to figure out constructor
                    emp.occupied_by = client.avatar
                    tile.occupied_by = emp
            case _:  # default case
                return
