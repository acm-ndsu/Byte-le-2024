from game.quarry_rush.map.collectable.collectable_generator import CollectableGenerator
from game.quarry_rush.map.game_location.game_location import GameLocation
from game.utils.vector import Vector
from game.common.game_object import GameObject


class MapGenerator:
    """
    Class used to generate entirety of map, including base stations, walls, ores, and ancient tech.
    """
    def __init__(self, seed: int = 8675309):
        self.__seed = seed
        self.__game_location = GameLocation()
        self.__collectable_generator = CollectableGenerator(self.__seed)

    def generate(self) -> dict[tuple[Vector], list[GameObject]]:
        """
        Calls generate methods and combines them to one dict using the update method. Returns the game map
        """
        game_location: dict[tuple[Vector], list[GameObject]] = self.__game_location.generate_location()
        collectables: dict[tuple[Vector], list[GameObject]] = self.__collectable_generator.generate_all()

        game_location.update(collectables)

        return game_location
