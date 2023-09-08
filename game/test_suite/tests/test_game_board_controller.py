import unittest
from unittest.mock import Mock
from game.controllers.game_board_controller import GameBoardController
from game.common.map.game_board import GameBoard

class TestGameBoardController(unittest.TestCase):
    """
    This class tests the GameBoard Controller
    """

    def setUp(self) -> None:
        self.game_board_controller: GameBoardController = GameBoardController()
        self.game_board: GameBoard = GameBoard()

    def test_pre_tick(self) -> None:
        mock: Mock = Mock()
        self.game_board.dynamite_detonation_control = mock

        self.game_board_controller.pre_tick(self.game_board)

        mock.assert_called_once()

    def test_post_tick(self) -> None:
        mock: Mock = Mock()
        self.game_board.trap_detonation_control = mock

        self.game_board_controller.post_tick(self.game_board)

        mock.assert_called_once()
