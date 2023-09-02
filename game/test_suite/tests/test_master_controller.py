import unittest

from game.controllers.master_controller import MasterController
from game.controllers.movement_controller import MovementController
from game.controllers.interact_controller import InteractController


class TestMasterController(unittest.TestCase):
    """
    `Test Master Controller Notes:`

        Add tests to this class to tests any new functionality added to the Master Controller.
    """

    def setUp(self) -> None:
        self.master_controller = MasterController()
        

