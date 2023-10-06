import unittest
from game.quarry_rush.station.company_station import ChurchStation, TuringStation
from game.utils.vector import Vector
from game.common.map.wall import Wall
from game.common.game_object import GameObject
from game.quarry_rush.map.map_generator import MapGenerator


class TestMapGenerator(unittest.TestCase):
    """
    Test Class for map_generator.py.
    """
    def setUp(self) -> None:
        self.map_generator: MapGenerator = MapGenerator(8675309)

    # Method to test if generation of entire game_map works.
    def test_map_generation(self) -> None:
        # Get dict for expected value for game locations
        expected: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1),): [Wall(), ], (Vector(4, 1),): [Wall(), ], (Vector(5, 1),): [Wall(), ],
            (Vector(20, 1),): [Wall(), ],
            (Vector(4, 2),): [Wall(), ], (Vector(4, 3),): [Wall(), ], (Vector(4, 4),): [Wall(), ],
            (Vector(9, 4),): [Wall(), ],
            (Vector(10, 4),): [Wall(), ], (Vector(11, 4),): [Wall(), ], (Vector(12, 4),): [Wall(), ],
            (Vector(13, 4),): [Wall(), ],
            (Vector(14, 4),): [Wall(), ], (Vector(15, 4),): [Wall(), ], (Vector(16, 4),): [Wall(), ],
            (Vector(4, 5),): [Wall(), ],
            (Vector(8, 5),): [Wall(), ], (Vector(9, 5),): [Wall(), ], (Vector(16, 5),): [Wall(), ],
            (Vector(17, 5),): [Wall(), ],
            (Vector(4, 6),): [Wall(), ], (Vector(8, 6),): [Wall(), ], (Vector(17, 6),): [Wall(), ],
            (Vector(4, 7),): [Wall(), ],
            (Vector(8, 7),): [Wall(), ], (Vector(17, 7),): [Wall(), ], (Vector(4, 8),): [Wall(), ],
            (Vector(17, 8),): [Wall(), ],
            (Vector(4, 9),): [Wall(), ], (Vector(17, 9),): [Wall(), ], (Vector(4, 10),): [Wall(), ],
            (Vector(17, 10),): [Wall(), ],
            (Vector(4, 11),): [Wall(), ], (Vector(17, 11),): [Wall(), ], (Vector(4, 12),): [Wall(), ],
            (Vector(17, 12),): [Wall(), ],
            (Vector(4, 13),): [Wall(), ], (Vector(17, 13),): [Wall(), ], (Vector(4, 14),): [Wall(), ],
            (Vector(13, 14),): [Wall(), ],
            (Vector(17, 14),): [Wall(), ], (Vector(4, 15),): [Wall(), ], (Vector(13, 15),): [Wall(), ],
            (Vector(17, 15),): [Wall(), ],
            (Vector(4, 16),): [Wall(), ], (Vector(5, 16),): [Wall(), ], (Vector(12, 16),): [Wall(), ],
            (Vector(13, 16),): [Wall(), ],
            (Vector(17, 16),): [Wall(), ], (Vector(5, 17),): [Wall(), ], (Vector(6, 17),): [Wall(), ],
            (Vector(7, 17),): [Wall(), ],
            (Vector(8, 17),): [Wall(), ], (Vector(9, 17),): [Wall(), ], (Vector(10, 17),): [Wall(), ],
            (Vector(11, 17),): [Wall(), ],
            (Vector(12, 17),): [Wall(), ], (Vector(17, 17),): [Wall(), ], (Vector(17, 18),): [Wall(), ],
            (Vector(17, 19),): [Wall(), ],
            (Vector(1, 20),): [Wall(), ], (Vector(16, 20),): [Wall(), ], (Vector(17, 20),): [Wall(), ],
            (Vector(20, 20),): [Wall(), ],
            (Vector(18, 18),): [TuringStation(), ], (Vector(19, 18),): [TuringStation(), ],
            (Vector(20, 18),): [TuringStation(), ],
            (Vector(18, 19),): [TuringStation(), ], (Vector(19, 19),): [TuringStation(), ],
            (Vector(20, 19),): [TuringStation(), ],
            (Vector(18, 20),): [TuringStation(), ], (Vector(19, 20),): [TuringStation(), ],
            (Vector(2, 1),): [ChurchStation(), ], (Vector(3, 1),): [ChurchStation(), ],
            (Vector(1, 2),): [ChurchStation(), ],
            (Vector(2, 2),): [ChurchStation(), ], (Vector(3, 2),): [ChurchStation(), ],
            (Vector(1, 3),): [ChurchStation(), ],
            (Vector(2, 3),): [ChurchStation(), ], (Vector(3, 3),): [ChurchStation(), ],
            # ADD ORE AND ANCIENT TECH OCCUPIABLE STATIONS HERE WITH EXACT LOCATIONS
        }

        # Get the actual result by calling the method
        actual: dict[tuple[Vector], list[GameObject]] = self.map_generator.generate()

        # compare all values within the dict to see if they match
        for (x, y), (i, j) in zip(expected.items(), actual.items()):
            for ake, bke in zip(x, i):
                self.assertEqual(ake.x, bke.x)
                self.assertEqual(ake.y, bke.y)
            for av, bv in zip(y, j):
                self.assertEqual(av.object_type, bv.object_type)

