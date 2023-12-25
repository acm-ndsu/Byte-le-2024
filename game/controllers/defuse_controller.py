from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller
from game.utils.vector import Vector


class DefuseController(Controller):
    def __init__(self) -> None:
        super().__init__()
        
    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        temp_vector: Vector
        match action:
            case ActionType.DEFUSE_UP:
                temp_vector = Vector(0, -1)
            case ActionType.DEFUSE_DOWN:
                temp_vector = Vector(0, 1)
            case ActionType.DEFUSE_LEFT:
                temp_vector = Vector(-1, 0)
            case ActionType.DEFUSE_RIGHT:
                temp_vector = Vector(1, 0)
            case _:
                return

        temp_vector.add_to_vector(client.avatar.position)
        world.defuse_trap_at(temp_vector)
