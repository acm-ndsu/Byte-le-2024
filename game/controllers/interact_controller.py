from game.common.enums import *
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.stations.station import Station
from game.common.items.item import Item
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector


class InteractController(Controller):
    """
    The Interact Controller manages the actions the player tries to execute. As the game is played, a player can
    interact with their surrounding, adjacent stations and the space they're currently standing on.

    x x x x x x
    x         x
    x   o     x
    x o P o   x
    x   o     x
    x x x x x x

    The given visual shows how players can interact. "P" represents the player; "o" represents the spaces that can be
    interacted with (included where the "P" is); and "x" represents the walls and map border.
    """

    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
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
        stat: Station = world.game_map[vector.y][vector.x].occupied_by

        if stat is not None and isinstance(stat, Station):
            stat.take_action(client.avatar)
