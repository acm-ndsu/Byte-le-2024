from game.controllers.controller import Controller
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.enums import *
from game.utils.vector import Vector


class MovementController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        avatar_pos: Vector = Vector(client.avatar.position.x, client.avatar.position.y)

        pos_mod: Vector
        match action:
            case ActionType.MOVE_UP:
                pos_mod = Vector(x=0, y=-1)
            case ActionType.MOVE_DOWN:
                pos_mod = Vector(x=0, y=1)
            case ActionType.MOVE_LEFT:
                pos_mod = Vector(x=-1, y=0)
            case ActionType.MOVE_RIGHT:
                pos_mod = Vector(x=1, y=0)
            case _:  # default case
                return

        temp_vec: Vector = Vector.add_vectors(avatar_pos, pos_mod)
        # if tile is occupied return
        temp: Tile = world.game_map[temp_vec.y][temp_vec.x]
        while hasattr(temp.occupied_by, 'occupied_by'):
            temp: Tile = temp.occupied_by
            
        if temp.occupied_by is not None:
            return 
        
        temp.occupied_by = client.avatar
        
        # while the object that occupies tile has the occupied by attribute, escalate check for avatar
        temp: Tile = world.game_map[avatar_pos.y][avatar_pos.x]
        while hasattr(temp.occupied_by, 'occupied_by'):
            temp = temp.occupied_by

        temp.occupied_by = None
        client.avatar.position = (temp_vec.x, temp_vec.y)
