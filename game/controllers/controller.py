from game.common.enums import DebugLevel, ActionType
from game.config import Debug
from game.common.player import Player
from game.common.map.game_board import GameBoard


class Controller:

    def __init__(self):
        self.debug_level = DebugLevel.controller
        self.debug = False

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        return

    def print(self, *args):
        if self.debug and Debug.level >= self.debug_level:
            print(f'{self.__class__.__name__}: ', end='')
            print(*args)
