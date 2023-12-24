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
                self.__place_dynamite(client, tile, world)
            case ActionType.PLACE_LANDMINE:
                self.__place_landmine(client, tile, world)
            case ActionType.PLACE_EMP:
                self.__place_emp(client, tile, world)
            case _:  # default case
                return

    def __place_dynamite(self, client: Player, tile: Tile, world: GameBoard) -> None:
        # places dynamite if the avatar's active ability allows it AND there isn't a dynamite object there already
        if client.avatar.can_place_dynamite() and not tile.is_occupied_by_object_type(ObjectType.DYNAMITE):
            dynamite: Dynamite = Dynamite(position=client.avatar.position, company=client.avatar.company)

            # place dynamite on top of the occupied_by stack but below the Avatar
            tile.place_on_top_of_stack(dynamite)
            world.dynamite_list.add_dynamite(dynamite)
            client.avatar.dynamite_active_ability.reset_fuse()  # reset the ability's cooldown

    def __place_landmine(self, client: Player, tile: Tile, world: GameBoard) -> None:
        # places a landmine if the avatar's active ability allows it AND there isn't a landmine object there already
        if client.avatar.can_place_landmine() and not tile.is_occupied_by_game_object(Trap):
            landmine: Landmine = Landmine(owner_company=client.avatar.company,
                                          target_company=client.avatar.get_opposing_team(),
                                          position=client.avatar.position)
            self.__add_to_trap_queue(client, world, landmine)

            # place a landmine on top of the occupied_by stack but below the Avatar
            tile.place_on_top_of_stack(landmine)

    def __place_emp(self, client: Player, tile: Tile, world: GameBoard) -> None:
        # places an EMP if the avatar's active ability allows it AND there isn't an EMP object there already
        if client.avatar.can_place_emp() and not tile.is_occupied_by_game_object(Trap):
            emp: EMP = EMP(owner_company=client.avatar.company,
                           target_company=client.avatar.get_opposing_team(), position=client.avatar.position)
            self.__add_to_trap_queue(client, world, emp)

            # place an EMP on top of the occupied_by stack but below the Avatar
            tile.place_on_top_of_stack(emp)

    def __add_to_trap_queue(self, client: Player, world: GameBoard, placed_object: Trap) -> None:
        # helper method that adds a trap to the correct trap queue depending on the avatar's company

        # reset the ability's cooldown based on which trap is set
        client.avatar.landmine_active_ability.reset_fuse() if isinstance(placed_object, Landmine) else \
            client.avatar.emp_active_ability.reset_fuse()

        # add the trap to the corresponding trap queue
        world.church_trap_queue.add_trap(placed_object) if client.avatar.company is Company.CHURCH else \
            world.turing_trap_queue.add_trap(placed_object)
