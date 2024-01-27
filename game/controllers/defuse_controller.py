from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller
from game.utils.vector import Vector
from game.config import TRAP_DEFUSAL_RANGE


class DefuseController(Controller):
    def __init__(self) -> None:
        super().__init__()
        
    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        if not client.avatar.can_defuse_trap():  # return if not usable
            return

        temp_vector: Vector
        match action:
            case ActionType.DEFUSE:
                all_poses = [Vector(x=x, y=y) for x in range(14) for y in range(14)]
                in_range = filter(lambda vec: vec.distance(client.avatar.position) <= TRAP_DEFUSAL_RANGE, all_poses)
                for vec in in_range:
                    world.defuse_trap_at(vec)
            case _:
                return
