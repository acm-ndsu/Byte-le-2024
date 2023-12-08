import unittest

from game.common.enums import ObjectType
from game.quarry_rush.station.company_station import ChurchStation, TuringStation
from game.utils.vector import Vector
from game.common.map.wall import Wall
from game.common.game_object import GameObject
from game.quarry_rush.map.map_generator import MapGenerator
from game.common.avatar import Avatar


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
            (Vector(4, 1),): [ChurchStation(), ],
            (Vector(9, 12),): [Avatar(), ],
            (Vector(4, 11),): [Avatar(), ],
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

        count = 0
        for key in actual.keys():
            if [z.object_type for z in actual[key]].__contains__(ObjectType.ORE_OCCUPIABLE_STATION):
                count += 1

        self.assertEqual(count, 100)