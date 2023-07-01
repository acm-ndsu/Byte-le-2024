from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.enums import *
from game.utils.vector import Vector
from game.controllers.controller import Controller


class GameBoardController(Controller):
    """
    This class is used to help maintain certain environmental changes on the game board. For example, there will
    be certain things that will only happen at the start or end of a turn.
    """

    def __init__(self):
        super().__init__()

    def pre_tick(self, client: Player, world: GameBoard):
        """
        This method will be called before the actions that need to take place during a turn.
        """

        # Uncomment this for when the dynamite list is completed
        # world.detonate_dynamite()
        pass

    def post_tick(self, client: Player, world: GameBoard):
        """
        This method will be called after all the actions of a turn are completed.
        """
        
        # world.detonate_traps()
        pass
