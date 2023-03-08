from game.common.enums import *
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.stations.station import Station
from game.common.items.item import Item
from game.common.map.game_board import GameBoard


class InteractController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client: Player, world: GameBoard):
        x: int = 0
        y: int = 0
        # match interaction type with x and y
        match (client.action):
            case ActionType.INTERACT_UP:
                x, y = 0, -1
            case ActionType.INTERACT_DOWN:
                x, y = 0, 1
            case ActionType.INTERACT_LEFT:
                x, y = -1, 0
            case ActionType.INTERACT_RIGHT:
                x, y = 1, 0
            case ActionType.INTERACT_CENTER:
                x, y = 0, 0
            case _:
                return
            
        # find result in interaction
        x += client.avatar.position[0]
        y += client.avatar.position[1]
        stat: Station = world.game_map[y][x].occupied_by

        if stat is not None and isinstance(stat, Station):
            result: Item|None = stat.take_action(client.avatar)

        client.avatar.held_item = result
