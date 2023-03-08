from game.controllers.controller import Controller
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.enums import *


class MovementController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client: Player, world: GameBoard):
        avatar_x: int = client.avatar.position[0]
        avatar_y: int = client.avatar.position[1]
        pos_mod: tuple[int,int] = (0,0)
        match client.action:
            case ActionType.MOVE_UP:
                pos_mod = (0, -1)
            case ActionType.MOVE_DOWN:
                pos_mod = (0, 1)
            case ActionType.MOVE_LEFT:
                pos_mod = (-1, 0)
            case ActionType.MOVE_RIGHT:
                pos_mod = (1, 0)
            case _:  # default case
                return

        # if tile is occupied return
        temp: Tile = world.game_map[avatar_y + pos_mod[1]][avatar_x + pos_mod[0]]
        while hasattr(temp.occupied_by, 'occupied_by'):
            temp: Tile = temp.occupied_by
            
        if temp.occupied_by is not None:
            return 
        
        temp.occupied_by = client.avatar
        
        # while the object that occupies tile has the occupied by attribute, escalate check for avatar
        temp: Tile = world.game_map[avatar_y][avatar_x]
        while hasattr(temp.occupied_by, 'occupied_by'):
            temp = temp.occupied_by

        temp.occupied_by = None
        client.avatar.position = (avatar_x + pos_mod[0], avatar_y + pos_mod[1])
