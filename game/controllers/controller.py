from game.common.enums import DebugLevel, ActionType
from game.config import Debug
from game.common.player import Player
from game.common.map.game_board import GameBoard
import logging


class Controller:
    """
    `Controller Class Notes:`

        This is a super class for every controller type that is necessary for inheritance. Think of it as the GameObject
        class for Controllers.

        The handle_actions method is important and will specify what each controller does when interacting with the
        Player object's avatar.

        Refer to the other controller files for a more detailed description on how they work.
        If more controllers are ever needed, add them to facilitate the flow of the game.
    """
    def __init__(self):
        self.debug_level = DebugLevel.CONTROLLER
        self.debug = False

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        return

    def debug(self, *args):
        if self.debug and Debug.level >= self.debug_level:
            logging.basicConfig(level=logging.DEBUGs)
            for arg in args:
                logging.debug(f'{self.__class__.__name__}: {arg}')
