from game.common.enums import *
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.map.occupiable import Occupiable
from game.common.map.tile import Tile
from game.common.player import Player
from game.controllers.controller import Controller
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.traps import Landmine, EMP
from game.utils.vector import Vector


class PlaceController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        avatar_pos: Vector = client.avatar.position
        tile: Tile = world.game_map[avatar_pos.x][avatar_pos.y]

        # depending on the action type, the type of placeable entity is placed on the map with the avatar occupying it
        match action:
            case ActionType.PLACE_DYNAMITE:
                self.__place_dyanmite(client, tile)
            case ActionType.PLACE_LANDMINE:
                self.__place_dyanmite(client, tile)
            case ActionType.PLACE_EMP:
                self.__place_emp(client, tile)
            case _:  # default case
                return

    def __place_dyanmite(self, client: Player, tile: Tile):
        # calls the place_on_top method to place a dynamite on top of the occupied_by stack but below the Avatar
        if client.avatar.can_place_dynamite():
            tile.place_on_top_of_stack(Dynamite())

    def __place_landmine(self, client: Player, tile: Tile):
        # calls the place_on_top method to place a landmine on top of the occupied_by stack but below the Avatar
        if client.avatar.can_place_trap():
            tile.place_on_top_of_stack(Landmine())

    def __place_emp(self, client: Player, tile: Tile):
        # calls the place_on_top method to place a dynamite on top of the occupied_by stack but below the Avatar
        if client.avatar.can_place_trap():
            tile.place_on_top_of_stack(EMP())
