from game.common.map.game_board import GameBoard
from game.controllers.controller import Controller
from game.common.avatar import Avatar
from game.common.enums import ObjectType


class GameBoardController(Controller):
    """
    This class is used to help maintain certain environmental changes on the game board. There will
    be certain things that will only happen at the start or end of a turn.
    """

    def __init__(self, world: GameBoard):
        super().__init__()
        self.world: GameBoard = world

    def pre_tick(self) -> None:
        """
        This method will be called before the actions that need to take place during a turn.
        """
        self.world.dynamite_detonation_control()

    def post_tick(self) -> None:
        """
        This method will be called after all the actions of a turn are completed.
        """
        self.world.trap_detonation_control()
