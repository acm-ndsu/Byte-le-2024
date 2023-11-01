from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.player import Player
from game.controllers.controller import Controller
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.traps import Landmine, EMP, Trap
from game.utils.vector import Vector


class PlaceController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard) -> None:
        avatar_pos: Vector = client.avatar.position
        tile: Tile = world.game_map[avatar_pos.x][avatar_pos.y]

        # depending on the action type, the type of placeable entity is placed on the map with the avatar occupying it
        match action:
            case ActionType.PLACE_DYNAMITE:
                self.__place_dyanmite(client, tile, world)
            case ActionType.PLACE_LANDMINE:
                self.__place_landmine(client, tile, world)
            case ActionType.PLACE_EMP:
                self.__place_emp(client, tile, world)
            case _:  # default case
                return

    def __place_dyanmite(self, client: Player, tile: Tile, world: GameBoard) -> None:
        # calls the place_on_top method to place a dynamite on top of the occupied_by stack but below the Avatar
        if client.avatar.can_place_dynamite():
            dynamite: Dynamite = Dynamite()
            tile.place_on_top_of_stack(dynamite)
            world.dynamite_list.add_dynamite(dynamite)
            client.avatar.dynamite_active_ability.reset_fuse()  # reset the ability's cooldown

    def __place_landmine(self, client: Player, tile: Tile, world: GameBoard) -> None:
        # calls the place_on_top method to place a landmine on top of the occupied_by stack but below the Avatar
        if client.avatar.can_place_trap():
            landmine: Landmine = Landmine()
            self.__add_to_trap_queue(client, world, landmine)
            tile.place_on_top_of_stack(Landmine())

    def __place_emp(self, client: Player, tile: Tile, world: GameBoard) -> None:
        # calls the place_on_top method to place a dynamite on top of the occupied_by stack but below the Avatar
        if client.avatar.can_place_trap():
            emp: EMP = EMP()
            self.__add_to_trap_queue(client, world, emp)
            tile.place_on_top_of_stack(emp)

    def __add_to_trap_queue(self, client: Player, world: GameBoard, placed_object: Trap) -> None:
        # helper method that adds a trap to the correct trap queue depending on the avatar's company

        client.avatar.place_trap.reset_fuse()  # reset the ability's cooldown

        match client.avatar.company:
            case Company.CHURCH:
                world.church_trap_queue.add_trap(placed_object)
            case Company.TURING:
                world.turing_trap_queue.add_trap(placed_object)
            case _:
                return
