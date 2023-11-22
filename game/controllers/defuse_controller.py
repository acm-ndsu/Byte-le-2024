from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller
from game.utils.vector import Vector


class DefuseController(Controller):
    def __init__(self) -> None:
        super().__init__()
        
    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        result_vector: Vector = client.avatar.position.add_to_vector(self.convert_to_vector(action))
        world.defuse_trap_at(result_vector)
        
    def convert_to_vector(self, action: ActionType) -> Vector:
        match action:
            case ActionType.DEFUSE_UP: return Vector(0, -1)
            case ActionType.DEFUSE_DOWN: return Vector(0, 1)
            case ActionType.DEFUSE_LEFT: return Vector(-1, 0)
            case ActionType.DEFUSE_RIGHT: return Vector(1, 0)
            case _: return Vector(0, 0)