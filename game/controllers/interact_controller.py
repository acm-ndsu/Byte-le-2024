from game.common.enums import *
from game.controllers.controller import Controller


class InteractController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client, world):
        stat = None
        x = None
        y = None
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
#                case ActionType.INTERACT_CENTER:
#                    x, y = 0, 0
            case _:
                return
        # find result in interaction
        if (x != None and y != None):
            x += client.avatar.position[0]
            y += client.avatar.position[1]
            stat = world.game_map[y][x].occupied_by
            if stat:
                result = stat.take_action(client.avatar)
            client.avatar.held_item = result
