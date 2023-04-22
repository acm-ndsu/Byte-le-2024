from game.common.enums import *
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.stations.station import Station
from game.common.items.item import Item
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector


class InteractController(Controller):

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
            result: Item | None = stat.take_action(client.avatar)
            client.avatar.held_item = result
