from json import load

from game.quarry_rush.map.collectable.collectable_weights_dict import COLLECTABLE_WEIGHTS
from game.utils.vector import Vector
from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation
import random as rand
import numpy as np
from perlin_noise import PerlinNoise


class CollectableGenerator:
    __board_size = 14  # This includes the borders. Field is 12x12
    __ore_count = 75

    def __init__(self, seed: int = rand.randint(0, 8675309)):
        collectable_weights = COLLECTABLE_WEIGHTS
        self.__ore_weights = collectable_weights['ore']
        self.__special_weights = collectable_weights['special']
        self.__ancient_tech_weights = collectable_weights['ancient_tech']
        self.__seed = seed

    def generate(self) -> dict[tuple[Vector], list[OreOccupiableStation]]:
        noise_map = self.adjust(self.layer(self.__ore_weights, self.generate_perlin_noise()))
        threshold = sorted([x for row in noise_map for x in row])[-self.__ore_count]
        ore_map = self.map_threshold(threshold, noise_map)

        def make_ore_station(x: int, y: int) -> list[OreOccupiableStation]:
            return [OreOccupiableStation(position=Vector(x=x, y=y),
                                         seed=self.__seed,
                                         special_weight=self.__special_weights[y][x],
                                         ancient_tech_weight=self.__ancient_tech_weights[y][x]), ]

        return {(Vector(x=x, y=y),): make_ore_station(x, y)
                for y, ore_row in enumerate(ore_map)
                for x, ore in enumerate(ore_row) if ore}

    def generate_random_noise(self) -> list[list[float]]:
        rng = np.random.default_rng(seed=self.__seed)
        return self.adjust(rng.random((self.__board_size,) * 2).tolist())

    def generate_perlin_noise(self) -> list[list[float]]:
        noise = PerlinNoise(octaves=8, seed=self.__seed)
        func = np.vectorize(lambda y, x: noise([x / self.__board_size, y / self.__board_size]))
        return self.adjust(np.fromfunction(func, (self.__board_size,) * 2).tolist())

    def adjust(self, raw: list[list[float]]) -> list[list[float]]:
        """
        Adjusts a weight map to be on the range [0..1]. This will always include 0 and 1 and maintain proportions
        """
        x = np.array(raw)
        return ((x - x.min()) / (x.max() - x.min())).tolist()

    def layer(self, layer1: list[list[float]], layer2: list[list[float]]) -> list[list[float]]:
        """
        Layers two weight maps on top of each other by multiplying each index individually
        """
        return (np.array(layer1) * np.array(layer2)).tolist()

    def map_threshold(self, threshold: float, weight_map: list[list[float]]) -> list[list[bool]]:
        """
        Takes a weight map and returns a new map of booleans where the value is True if the
        value in the original map is >= the threshold
        """
        return (np.array(weight_map) >= threshold).tolist()
