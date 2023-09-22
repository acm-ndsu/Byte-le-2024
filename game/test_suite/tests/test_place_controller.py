import unittest

from game.quarry_rush.entity.placeable.trap import *
from game.common.enums import Company
from game.utils.vector import Vector
from game.controllers.place_controller import *


class TestPlaceController(unittest.TestCase):
    """
    This class is to test the TestPlaceController and placing Dynamite, Landmines, and EMPs on the GameBoard
    """

    def setUp(self):
        self.place_controller: PlaceController = PlaceController()

