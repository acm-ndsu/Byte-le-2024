from game.common.enums import *
from game.common.game_object import GameObject
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.stations.station import Station
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector
from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation


class InteractController(Controller):
    """
    `Interact Controller Notes:`

        The Interact Controller manages the actions the player tries to execute. As the game is played, a player can
        interact with surrounding, adjacent stations and the space they're currently standing on.

        Example:
        ::
            x x x x x x
            x         x
            x   O     x
            x O A O   x
            x   O     x
            x x x x x x

        The given visual shows what players can interact with. "A" represents the avatar; "O" represents the spaces
        that can be interacted with (including where the "A" is); and "x" represents the walls and map border.

        These interactions are managed by using the provided ActionType enums in the enums.py file.
    """

    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard, target: GameObject | ObjectType = Station()) -> None:
        """
        Given the ActionType for interacting in a direction, the Player's avatar will engage with the object.
        :param action:
        :param client:
        :param world:
        :param target:
        :return: None
        """

        # match interaction type with x and y
        vector: Vector
        match action:
            case ActionType.INTERACT_UP:
                vector = Vector(x=0, y=-1)
            case ActionType.INTERACT_DOWN:
                vector = Vector(x=0, y=1)
            case ActionType.INTERACT_LEFT:
                vector = Vector(x=-1, y=0)
            case ActionType.INTERACT_RIGHT:
                vector = Vector(x=1, y=0)
            case ActionType.INTERACT_CENTER:
                vector = Vector(0, 0)
            case _:
                return
            
        # find result in interaction
        vector.x += client.avatar.position.x
        vector.y += client.avatar.position.y

        stat: Station | None = world.game_map[vector.y][vector.x].get_occupied_by(target)

        if stat is not None and isinstance(stat, Station) and not isinstance(stat, OreOccupiableStation):
            stat.take_action(client.avatar, world.inventory_manager)
