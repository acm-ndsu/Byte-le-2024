import unittest

from game.common.enums import ObjectType
from game.quarry_rush.station.company_station import ChurchStation, TuringStation
from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation
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
            (Vector(x=5, y=1),): [Wall(), ],
            (Vector(x=6, y=1),): [Wall(), ],
            (Vector(x=12, y=1),): [Wall(), ],
            (Vector(x=4, y=2),): [Wall(), ],
            (Vector(x=5, y=2),): [Wall(), ],
            (Vector(x=3, y=3),): [Wall(), ],
            (Vector(x=4, y=3),): [Wall(), ],
            (Vector(x=9, y=3),): [Wall(), ],
            (Vector(x=3, y=4),): [Wall(), ],
            (Vector(x=9, y=4),): [Wall(), ],
            (Vector(x=10, y=4),): [Wall(), ],
            (Vector(x=3, y=5),): [Wall(), ],
            (Vector(x=10, y=5),): [Wall(), ],
            (Vector(x=3, y=6),): [Wall(), ],
            (Vector(x=10, y=6),): [Wall(), ],
            (Vector(x=3, y=7),): [Wall(), ],
            (Vector(x=10, y=7),): [Wall(), ],
            (Vector(x=3, y=8),): [Wall(), ],
            (Vector(x=10, y=8),): [Wall(), ],
            (Vector(x=3, y=9),): [Wall(), ],
            (Vector(x=4, y=9),): [Wall(), ],
            (Vector(x=10, y=9),): [Wall(), ],
            (Vector(x=4, y=10),): [Wall(), ],
            (Vector(x=9, y=10),): [Wall(), ],
            (Vector(x=10, y=10),): [Wall(), ],
            (Vector(x=8, y=11),): [Wall(), ],
            (Vector(x=9, y=11),): [Wall(), ],
            (Vector(x=1, y=12),): [Wall(), ],
            (Vector(x=7, y=12),): [Wall(), ],
            (Vector(x=8, y=12),): [Wall(), ],
            (Vector(x=9, y=12),): [TuringStation(), ],
            (Vector(x=4, y=1),): [ChurchStation(), ],
            (Vector(9, 12),): [Avatar(), ],
            (Vector(4, 1),): [Avatar(), ]
        }

        # Get the actual result by calling the method
        actual: dict[tuple[Vector], list[GameObject]] = self.map_generator.generate()


        # compare all values within the dict to see if they match (ignoring ORE_OCCUPIABLE_STATIONs)
        for (x, y), (i, j) in zip(expected.items(), dict(filter(lambda pair : pair[1][0].object_type != ObjectType.ORE_OCCUPIABLE_STATION, actual.items())).items()):
            for ake, bke in zip(x, i):
                self.assertEqual(ake.x, bke.x)
                self.assertEqual(ake.y, bke.y)
            for av, bv in zip(y, j):
                self.assertEqual(av.object_type, bv.object_type)

        # check if there are exactly 75 ORE_OCCUPIABLE_STATIONS
        count = 0
        for key in actual.keys():
            if [z.object_type for z in actual[key]].__contains__(ObjectType.ORE_OCCUPIABLE_STATION):
                count += 1

        self.assertEqual(count, 100)
