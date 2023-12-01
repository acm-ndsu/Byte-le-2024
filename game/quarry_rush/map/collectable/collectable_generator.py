from json import load
from game.utils.vector import Vector
from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation
import random as rand
from typing import TypeAlias
from perlin_noise import PerlinNoise

CollectableStation: TypeAlias = OreOccupiableStation


class CollectableGenerator:
    __board_size = 14  # This includes the borders. Field is 20x20
    __copium_count = 50  # This is the number of copium that should be generated
    __special_count = 25  # This is the number of each special ore that should be generated (50 means 50 lambdium and 50 turite)
    __ancient_tech_count = 50  # This is the number of ancient tech that should be generated

    def __init__(self, seed: int = rand.randint(0, 8675309)):
        f = open('game/quarry_rush/map/collectable/collectable_weights.json')
        collectable_weights = load(f)
        f.close()

        self.__copium_weights = collectable_weights['copium']
        self.__lambdium_weights = collectable_weights['special']
        self.__turite_weights = collectable_weights['special']
        self.__ancient_tech_weights = collectable_weights['ancient_tech']
        self.__seed = seed

    def generate_copium(self) -> list[list[bool]]:
        """
        Returns a 2D list of bools describing where to put copium.
        Will not overlap with walls or bases.
        """
        noise_map = self.adjust(self.layer(self.__copium_weights, self.generate_perlin_noise()))
        threshold = sorted([x for row in noise_map for x in row])[-self.__copium_count]
        return self.map_threshold(threshold, noise_map)

    def generate_lambdium(self) -> list[list[bool]]:
        """
        Returns a 2D list of bools describing where to put lambdium.
        Will not overlap with walls or bases.
        """
        noise_map = self.adjust(self.layer(self.__lambdium_weights, self.generate_perlin_noise()))
        threshold = sorted([x for row in noise_map for x in row])[-self.__special_count]
        return self.map_threshold(threshold, noise_map)

    def generate_turite(self) -> list[list[bool]]:
        """
        Returns a 2D list of bools describing where to put turite.
        Will not overlap with walls or bases.
        """
        noise_map = self.adjust(self.layer(self.__turite_weights, self.generate_perlin_noise()))
        threshold = sorted([x for row in noise_map for x in row])[-self.__special_count]
        return self.map_threshold(threshold, noise_map)

    def generate_ancient_tech(self) -> list[list[bool]]:
        """
        Returns a 2D list of bools describing where to put ancient tech.
        Will not overlap with walls or bases.
        """
        noise_map = self.adjust(self.layer(self.__ancient_tech_weights, self.generate_random_noise()))
        threshold = sorted([x for row in noise_map for x in row])[-self.__ancient_tech_count]
        return self.map_threshold(threshold, noise_map)

    def generate_all(self) -> dict[tuple[Vector]: list[CollectableStation]]:
        copium_map = self.generate_copium()
        lambdium_map = self.generate_lambdium()
        turite_map = self.generate_turite()
        ancient_tech_map = self.generate_ancient_tech()

        result: dict[tuple[Vector]: list[CollectableStation]] = {}
        # for (y, x) in [(y, x) for y in range(self.__board_size) for x in range(self.__board_size)]:
        #     stations: list[CollectableStation] = []
        #     if copium_map[y][x]:
        #         stations.append(CopiumOccupiableStation())
        #     if lambdium_map[y][x]:
        #         stations.append(LambdiumOccupiableStation())
        #     if turite_map[y][x]:
        #         stations.append(TuriteOccupiableStation())
        #     if ancient_tech_map[y][x]:
        #         stations.append(AncientTechOccupiableStation())
        #     if len(stations) > 0:
        #         result[(Vector(x=x, y=y),)] = stations
        return result

    def generate_random_noise(self) -> list[list[float]]:
        rand.seed(self.__seed)
        self.__seed += 1
        raw = [[rand.random() for x in range(self.__board_size)] for y in range(self.__board_size)]
        return self.adjust(raw)

    def generate_perlin_noise(self) -> list[list[float]]:
        noise = PerlinNoise(octaves=8, seed=self.__seed)
        self.__seed += 1
        return self.adjust(
            [[noise([x / self.__board_size, y / self.__board_size]) for x in range(self.__board_size)] for y in range(self.__board_size)])

    def adjust(self, raw: list[list[float]]) -> list[list[float]]:
        """
        Adjusts a weight map to be on the range [0..1]. This will always include 0 and 1 and maintain proportions
        """
        minimum = min(map(min, raw))
        maximum = max(map(max, raw))
        mapper = lambda x: (1 / (maximum - minimum)) * (x - minimum)
        return list(map(lambda xs: list(map(mapper, xs)), raw))

    def layer(self, layer1: list[list[float]], layer2: list[list[float]]) -> list[list[float]]:
        """
        Layers two weight maps on top of each other by multiplying each index individually
        """
        return [[layer1[y][x] * layer2[y][x] for x in range(self.__board_size)] for y in range(self.__board_size)]

    def map_threshold(self, threshold: float, weight_map: list[list[float]]) -> list[list[bool]]:
        """
        Takes a weight map and returns a new map of booleans where the value is True if the
        value in the original map is >= the threshold
        """
        return list(map(lambda xs: list(map(lambda x: x >= threshold, xs)), weight_map))
