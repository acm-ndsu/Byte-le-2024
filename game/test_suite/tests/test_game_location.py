import unittest

from game.quarry_rush.map.game_location.game_location import GameLocation
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.map.wall import Wall
from game.quarry_rush.station.company_station import ChurchStation, TuringStation


class TestGameLocation(unittest.TestCase):
    """
    Test class for game_location.py.
    """

    def setUp(self) -> None:
        self.game_location: GameLocation = GameLocation()

    # Method to test if generation of game_locations works
    def test_game_locations(self) -> None:
        # Get dict for expected value for game locations
        expected: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(5, 1),): [Wall(), ], (Vector(6, 1),): [Wall(), ], (Vector(12, 1),): [Wall(), ],
            (Vector(4, 2),): [Wall(), ], (Vector(5, 2),): [Wall(), ],
            (Vector(3, 3),): [Wall(), ], (Vector(4, 3),): [Wall(), ], (Vector(9, 3),): [Wall(), ],
            (Vector(3, 4),): [Wall(), ], (Vector(9, 4),): [Wall(), ], (Vector(10, 4),): [Wall(), ],
            (Vector(3, 5),): [Wall(), ], (Vector(10, 5),): [Wall(), ],
            (Vector(3, 6),): [Wall(), ], (Vector(10, 6),): [Wall(), ],
            (Vector(3, 7),): [Wall(), ], (Vector(10, 7),): [Wall(), ],
            (Vector(3, 8),): [Wall(), ], (Vector(10, 8),): [Wall(), ],
            (Vector(3, 9),): [Wall(), ], (Vector(4, 9),): [Wall(), ], (Vector(10, 9),): [Wall(), ],
            (Vector(4, 10),): [Wall(), ], (Vector(9, 10),): [Wall(), ], (Vector(10, 10),): [Wall(), ],
            (Vector(8, 11),): [Wall(), ], (Vector(9, 11),): [Wall(), ],
            (Vector(1, 12),): [Wall(), ], (Vector(7, 12),): [Wall(), ], (Vector(8, 12),): [Wall(), ],
            (Vector(9, 12),): [TuringStation(), ],
            (Vector(4, 1),): [ChurchStation(), ]
        }

        # Get the actual result by calling the method
        actual: dict[tuple[Vector], list[GameObject]] = self.game_location.generate_location()
        # compare all values within the dict to see if they match
        for (x, y), (i, j) in zip(expected.items(), actual.items()):
            for ake, bke in zip(x, i):
                self.assertEqual(ake.x, bke.x)
                self.assertEqual(ake.y, bke.y)
            for av, bv in zip(y, j):
                self.assertEqual(av.object_type, bv.object_type)
