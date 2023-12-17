from json import load
from game.utils.vector import Vector
from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation
import random as rand
from typing import TypeAlias
from perlin_noise import PerlinNoise


class CollectableGenerator:
    __board_size = 14  # This includes the borders. Field is 20x20
    __ore_count = 100

    def __init__(self, seed: int = rand.randint(0, 8675309)):
        f = open('game/quarry_rush/map/collectable/collectable_weights.json')
        collectable_weights = load(f)
        f.close()

        self.__ore_weights = collectable_weights['ore']
        self.__special_weights = collectable_weights['special']
        self.__ancient_tech_weights = collectable_weights['ancient_tech']
        self.__seed = seed
        
    def generate(self) -> dict[tuple[Vector], OreOccupiableStation]:
        noise_map = self.adjust(self.layer(self.__ore_weights, self.generate_perlin_noise()))
        threshold = sorted([x for row in noise_map for x in row])[-self.__ore_count]
        ore_map = self.map_threshold(threshold, noise_map)
        
        result: dict[tuple[Vector], OreOccupiableStation] = {}
        for y in range(len(ore_map)):
            for x in range(len(ore_map[y])):
                if ore_map[y][x]:
                    vec = Vector(x=x, y=y)
                    result[(vec,)] = [ OreOccupiableStation(position=vec,
                                                          seed=self.__seed,
                                                          special_weight=self.__special_weights[y][x],
                                                          ancient_tech_weight=self.__ancient_tech_weights[y][x]), ]
        return result
    

    def generate_random_noise(self) -> list[list[float]]:
        rand.seed(self.__seed)
        raw = [[rand.random() for x in range(self.__board_size)] for y in range(self.__board_size)]
        return self.adjust(raw)

    def generate_perlin_noise(self) -> list[list[float]]:
        noise = PerlinNoise(octaves=8, seed=self.__seed)
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
