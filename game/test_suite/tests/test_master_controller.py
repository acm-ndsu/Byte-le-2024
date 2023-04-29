import unittest

from game.controllers.master_controller import MasterController
from game.controllers.movement_controller import MovementController
from game.controllers.interact_controller import InteractController


class TestMasterController(unittest.TestCase):
    def setUp(self) -> None:
        self.master_controller = MasterController()
        

