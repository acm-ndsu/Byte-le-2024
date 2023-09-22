from json import load
import random as rand
from perlin_noise import PerlinNoise

class CollectableGenerator:
    
    board_size = 22 # This includes the borders. Field is 20x20 
    threshold = 0.3 # Threshold of 0 will have every tile filled with ore, threshold of 1 will have no tiles with ore
    
    def __init__(self, seed: int = rand.randint(0, 8675309)):
        f = open('game/quarry_rush/map/collectable/collectable_weights.json')
        collectable_weights = load(f)
        f.close()
        
        self.__copium_weights = collectable_weights['copium']
        self.__lambdium_weights = collectable_weights['lambdium']
        self.__turite_weights = collectable_weights['turite']
        self.__ancient_tech_weights = collectable_weights['ancient_tech']
        self.__seed = seed
        
    def generate_copium(self) -> list[list[bool]]:
        '''
        Returns a 2D list of bools describing where to put copium.
        Will not overlap with walls or bases.
        '''
        # TODO use perlin noise
        return self.map_threshold(self.adjust(self.layer(self.__copium_weights, self.generate_random_noise())))
    
    def generate_lambdium(self) -> list[list[bool]]:
        '''
        Returns a 2D list of bools describing where to put lambdium.
        Will not overlap with walls or bases.
        '''
        # TODO use perlin noise
        return self.map_threshold(self.adjust(self.layer(self.__lambdium_weights, self.generate_random_noise())))
    
    def generate_turite(self) -> list[list[bool]]:
        '''
        Returns a 2D list of bools describing where to put turite.
        Will not overlap with walls or bases.
        '''
        # TODO use perlin noise
        return self.map_threshold(self.adjust(self.layer(self.__turite_weights, self.generate_random_noise())))
    
    def generate_ancient_tech(self) -> list[list[bool]]:
        '''
        Returns a 2D list of bools describing where to put ancient tech.
        Will not overlap with walls or bases.
        '''
        # TODO use perlin noise
        return self.map_threshold(self.adjust(self.layer(self.__ancient_tech_weights, self.generate_random_noise())))
    
    def generate_all(self):
        # generate lambdium
        # generate turite
        # TODO: handle overlap between lambdium and turite
        # generate ancient tech
        # generate copium
        
        # stuff cannot override stuff from previous step(s) in this section of the algorithm
        # put lambdium and turite into result map
        # TODO: should ancient tech be allowed to overlap? if not, put ancient tech into result map
        # put copium into result map
        
        # return result map
        pass
    
    def generate_random_noise(self) -> list[list[float]]:
        rand.seed(self.__seed)
        raw = [[rand.random() for x in range(self.board_size)] for y in range(self.board_size)]
        return self.adjust(raw)
        
    def generate_perlin_noise(self) -> list[list[float]]:
        noise = PerlinNoise(octaves=8, seed=self.__seed)
        self.__seed += 1
        return self.adjust([[noise([x/22, y/22]) for x in range(self.board_size)] for y in range(self.board_size)])
    
    def adjust(self, raw: list[list[float]]) -> list[list[float]]:
        '''
        Adjusts a weight map to be on the range [0..1]. This will always include 0 and 1 and maintain proportions
        '''
        minimum = min(map(min, raw))
        maximum = max(map(max, raw))
        mapper = lambda x : (1 / (maximum - minimum)) * (x - minimum)
        return list(map(lambda xs : list(map(mapper, xs)), raw))
    
    def layer(self, layer1: list[list[float]], layer2: list[list[float]]) -> list[list[float]]:
        '''
        Layers two weight maps on top of each other by multiplying each index individually
        '''
        return [[layer1[y][x] * layer2[y][x] for x in self.board_size] for y in self.board_size]
    
    def map_threshold(self, weight_map: list[list[float]]) -> list[list[bool]]:
        '''
        Takes a weight map and returns a new map of booleans where the value is True if the
        value in the original map is >= the threshold
        '''
        return list(map(lambda xs : list(map(lambda x : x >= self.threshold, xs)), weight_map))