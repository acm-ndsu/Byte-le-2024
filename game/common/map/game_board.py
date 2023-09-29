import random
from typing import Self, Callable

from game.common.avatar import Avatar
from game.common.enums import *
from game.common.game_object import GameObject
from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.station import Station
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.utils.vector import Vector
from game.quarry_rush.entity.placeable.traps import Trap


class TrapQueue(GameObject):
    def __init__(self):
        super().__init__()
        self.__traps: list[Trap] = []
        self.__max_traps = 10

    def add_trap(self, trap: Trap):
        if len(self.__traps) >= self.__max_traps:
            self.__traps = self.__traps[1:]
        self.__traps += [trap]
        
    def detonate(self, inventory_manager: InventoryManager):
        for i in range(0, len(self.__traps))[::-1]:
            if self.__traps[i].detonate(inventory_manager):
                self.__traps = self.__traps[:i] + self.__traps[i+1:]

    def size(self) -> int:
        return len(self.__traps)

    def to_json(self):
        data = super().to_json()
        data['traps'] = list(map(lambda t: t.to_json(), self.__traps))
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__traps = list(map(lambda t: Trap().from_json(t), data['traps']))
        return self


class DynamiteList(GameObject):
    """
    A list for storing dynamite on the game_board. It is different from the TrapQueue because placing dynamite on the
    map is balanced by the cooldown given by the active ability. There won't be a max size for this.
    """

    def __init__(self):
        super().__init__()
        self.__dynamite_list: list[Dynamite] = []

    def add_dynamite(self, dynamite: Dynamite):
        self.__dynamite_list.append(dynamite)

    def detonate(self, inventory_manager: InventoryManager):
        for dynamite in self.__dynamite_list:
            if dynamite.detonate(inventory_manager):
                self.__dynamite_list.remove(dynamite)

    def size(self) -> int:
        return len(self.__dynamite_list)

    def get_from_list(self, index: int) -> Dynamite:
        return self.__dynamite_list[index]

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['dynamite_items'] = list(map(lambda dynamite: dynamite.to_json(), self.__dynamite_list))
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__dynamite_list: list[Dynamite] = list(map(lambda d: Dynamite().from_json(d),
                                                        data['dynamite_items']))
        return self


class GameBoard(GameObject):
    """
    `GameBoard Class Notes:`

    Map Size:
    ---------
        map_size is a Vector object, allowing you to specify the size of the (x, y) plane of the game board.
        For example, a Vector object with an 'x' of 5 and a 'y' of 7 will create a board 5 tiles wide and
        7 tiles long.

        Example:
        ::
            _ _ _ _ _  y = 0
            |       |
            |       |
            |       |
            |       |
            |       |
            |       |
            _ _ _ _ _  y = 6

    -----

    Locations:
    ----------
        This is the bulkiest part of the generation.

        The locations field is a dictionary with a key of a tuple of Vectors, and the value being a list of
        GameObjects (the key **must** be a tuple instead of a list because Python requires dictionary keys to be
        immutable).

        This is used to assign the given GameObjects the given coordinates via the Vectors. This is done in two ways:

        Statically:
            If you want a GameObject to be at a specific coordinate, ensure that the key-value pair is
            *ONE* Vector and *ONE* GameObject.
            An example of this would be the following:
            ::
                locations = { (vector_2_4) : [station_0] }

            In this example, vector_2_4 contains the coordinates (2, 4). (Note that this naming convention
            isn't necessary, but was used to help with the concept). Furthermore, station_0 is the
            GameObject that will be at coordinates (2, 4).

        Dynamically:
            If you want to assign multiple GameObjects to different coordinates, use a key-value
            pair of any length.

            **NOTE**: The length of the tuple and list *MUST* be equal, otherwise it will not
            work. In this case, the assignments will be random. An example of this would be the following:
            ::
                locations =
                {
                    (vector_0_0, vector_1_1, vector_2_2) : [station_0, station_1, station_2]
                }

            (Note that the tuple and list both have a length of 3).

            When this is passed in, the three different vectors containing coordinates (0, 0), (1, 1), or
            (2, 2) will be randomly assigned station_0, station_1, or station_2.

            If station_0 is randomly assigned at (1, 1), station_1 could be at (2, 2), then station_2 will be at (0, 0).
            This is just one case of what could happen.

        Lastly, another example will be shown to explain that you can combine both static and
        dynamic assignments in the same dictionary:
        ::
            locations =
                {
                    (vector_0_0) : [station_0],
                    (vector_0_1) : [station_1],
                    (vector_1_1, vector_1_2, vector_1_3) : [station_2, station_3, station_4]
                }

        In this example, station_0 will be at vector_0_0 without interference. The same applies to
        station_1 and vector_0_1. However, for vector_1_1, vector_1_2, and vector_1_3, they will randomly
        be assigned station_2, station_3, and station_4.

    -----

    Walled:
    -------
        This is simply a bool value that will create a wall barrier on the boundary of the game_board. If
        walled is True, the wall will be created for you.

        For example, let the dimensions of the map be (5, 7). There will be wall Objects horizontally across
        x = 0 and x = 4. There will also be wall Objects vertically at y = 0 and y = 6

        Below is a visual example of this, with 'x' being where the wall Objects are.

        Example:
        ::
            x x x x x   y = 0
            x       x
            x       x
            x       x
            x       x
            x       x
            x x x x x   y = 6
    """

    def __init__(self, seed: int | None = None, map_size: Vector = Vector(),
                 locations: dict[tuple[Vector]:list[GameObject]] | None = None, walled: bool = False):

        super().__init__()
        # game_map is initially going to be None. Since generation is slow, call generate_map() as needed
        self.game_map: list[list[Tile]] | None = None
        self.seed: int | None = seed
        random.seed(seed)
        self.object_type: ObjectType = ObjectType.GAMEBOARD
        self.event_active: int | None = None
        self.map_size: Vector = map_size
        # when passing Vectors as a tuple, end the tuple of Vectors with a comma so it is recognized as a tuple
        self.locations: dict | None = locations
        self.walled: bool = walled
        self.inventory_manager: InventoryManager = InventoryManager()
        self.church_trap_queue = TrapQueue()
        self.turing_trap_queue = TrapQueue()
        self.dynamite_list: DynamiteList = DynamiteList()

    @property
    def seed(self) -> int:
        return self.__seed

    @seed.setter
    def seed(self, seed: int | None) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if seed is not None and not isinstance(seed, int):
            raise ValueError(f'{self.__class__.__name__}.seed must be an integer or None.')
        self.__seed = seed

    @property
    def game_map(self) -> list[list[Tile]] | None:
        return self.__game_map

    @game_map.setter
    def game_map(self, game_map: list[list[Tile]]) -> None:
        if game_map is not None and (not isinstance(game_map, list) or
                                     any(map(lambda l: not isinstance(l, list), game_map)) or
                                     any([any(map(lambda g: not isinstance(g, Tile), tile_list))
                                          for tile_list in game_map])):
            raise ValueError(f'{self.__class__.__name__}.game_map must be a list[list[Tile]].')
        self.__game_map = game_map

    @property
    def map_size(self) -> Vector:
        return self.__map_size

    @map_size.setter
    def map_size(self, map_size: Vector) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if map_size is None or not isinstance(map_size, Vector):
            raise ValueError(f'{self.__class__.__name__}.map_size must be a Vector.')
        self.__map_size = map_size

    @property
    def locations(self) -> dict:
        return self.__locations

    @locations.setter
    def locations(self, locations: dict[tuple[Vector]:list[GameObject]] | None) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if locations is not None and not isinstance(locations, dict):
            raise ValueError("Locations must be a dict. The key must be a tuple of Vector Objects, and the "
                             "value a list of GameObject.")
        # if locations is not None:
        #     for k, v in locations.items():
        #         if len(k) != len(v):
        #             raise ValueError("Cannot set the locations for the game_board. A key has a different "
        #                              "length than its key.")

        self.__locations = locations

    @property
    def walled(self) -> bool:
        return self.__walled

    @walled.setter
    def walled(self, walled: bool) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if walled is None or not isinstance(walled, bool):
            raise ValueError(f'{self.__class__.__name__}.walled must be a bool.')

        self.__walled = walled

    def generate_map(self) -> None:
        # generate map
        self.game_map = [[Tile() for _ in range(self.map_size.x)] for _ in range(self.map_size.y)]

        if self.walled:
            for x in range(self.map_size.x):
                if x == 0 or x == self.map_size.x - 1:
                    for y in range(self.map_size.y):
                        self.game_map[y][x].occupied_by = Wall()
                self.game_map[0][x].occupied_by = Wall()
                self.game_map[self.map_size.y - 1][x].occupied_by = Wall()

        self.__populate_map()

    def __populate_map(self) -> None:
        for k, v in self.locations.items():
            if len(k) == 0 or len(v) == 0:  # Key-Value lengths must be > 0 and equal
                raise ValueError("A key-value pair from game_board.locations has a length of 0. ")

            # random.sample returns a randomized list which is used in __help_populate()
            j = random.sample(k, k=len(k))
            self.__help_populate(j, v)

    def __occupied_filter(self, game_object_list: list[GameObject]) -> list[GameObject]:
        """
        A helper method that returns a list of game objects that have the 'occupied_by' attribute.
        :param game_object_list:
        :return: a list of game object
        """
        return [game_object for game_object in game_object_list if hasattr(game_object, 'occupied_by')]

    def __help_populate(self, vector_list: list[Vector], game_object_list: list[GameObject]) -> None:
        """
        A helper method that helps populate the game map.
        :param vector_list:
        :param game_object_list:
        :return: None
        """

        zipped_list: [tuple[list[Vector], list[GameObject]]] = list(zip(vector_list, game_object_list))
        last_vec: Vector = zipped_list[-1][0]

        remaining_objects: list[GameObject] | None = self.__occupied_filter(game_object_list[len(zipped_list):]) \
            if len(self.__occupied_filter(game_object_list)) > len(zipped_list) \
            else None

        # Will cap at smallest list when zipping two together
        for vector, game_object in zipped_list:
            if isinstance(game_object, Avatar):  # If the GameObject is an Avatar, assign it the coordinate position
                game_object.position = vector

            temp_tile: GameObject = self.game_map[vector.y][vector.x]

            while hasattr(temp_tile.occupied_by, 'occupied_by'):
                temp_tile = temp_tile.occupied_by

            if temp_tile is None:
                raise ValueError("Last item on the given tile doesn't have the 'occupied_by' attribute.")

            temp_tile.occupied_by = game_object

        if remaining_objects is None:
            return

        # stack remaining game_objects on last vector
        temp_tile: GameObject = self.game_map[last_vec.y][last_vec.x]

        while hasattr(temp_tile.occupied_by, 'occupied_by'):
            temp_tile = temp_tile.occupied_by

        for game_object in remaining_objects:
            if temp_tile is None:
                raise ValueError("Last item on the given tile doesn't have the 'occupied_by' attribute.")

            temp_tile.occupied_by = game_object
            temp_tile = temp_tile.occupied_by

    def get_objects(self, look_for: ObjectType) -> list[tuple[Vector, list[GameObject]]]:
        to_return: list[tuple[Vector, list[GameObject]]] = list()

        for y, row in enumerate(self.game_map):
            for x, object_in_row in enumerate(row):
                go_list: list[GameObject] = []
                temp: GameObject = object_in_row
                self.__get_objects_help(look_for, temp, go_list)
                if len(go_list) > 0:
                    to_return.append((Vector(x=x, y=y), [*go_list, ]))

        return to_return

    def __get_objects_help(self, look_for: ObjectType, temp: GameObject | Tile, to_return: list[GameObject]):
        while hasattr(temp, 'occupied_by'):
            if temp.object_type is look_for:
                to_return.append(temp)

            # The final temp is the last occupied by option which is either an Avatar, Station, or None
            temp = temp.occupied_by

        if temp is not None and temp.object_type is look_for:
            to_return.append(temp)

    def to_json(self) -> dict:
        data: dict[str, object] = super().to_json()
        temp: list[list[Tile]] = list(
            list(map(lambda tile: tile.to_json(), y)) for y in self.game_map) if self.game_map is not None else None
        data["game_map"] = temp
        data["seed"] = self.seed
        data["map_size"] = self.map_size.to_json()
        data["location_vectors"] = [[vec.to_json() for vec in k] for k in
                                    self.locations.keys()] if self.locations is not None else None
        data["location_objects"] = [[obj.to_json() for obj in v] for v in
                                    self.locations.values()] if self.locations is not None else None
        data["walled"] = self.walled
        data['event_active'] = self.event_active
        data['inventory_manager'] = self.inventory_manager.to_json()
        data['church_trap_queue'] = self.church_trap_queue.to_json()
        data['turing_trap_queue'] = self.turing_trap_queue.to_json()
        data['dynamite_list'] = self.dynamite_list.to_json()
        return data

    def generate_event(self, start: int, end: int) -> None:
        self.event_active = random.randint(start, end)

    def __from_json_helper(self, data: dict) -> GameObject:
        temp: ObjectType = ObjectType(data['object_type'])
        match temp:
            case ObjectType.WALL:
                return Wall().from_json(data)
            case ObjectType.OCCUPIABLE_STATION:
                return OccupiableStation().from_json(data)
            case ObjectType.STATION:
                return Station().from_json(data)
            case ObjectType.AVATAR:
                return Avatar().from_json(data)
            # If adding more ObjectTypes that can be placed on the game_board, specify here
            case _:
                raise ValueError(f'The location (dict) must have a valid key (tuple of vectors) and a valid value ('
                                 f'list of GameObjects).')

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        temp = data['game_map']
        self.seed: int | None = data['seed']
        self.map_size: Vector = Vector().from_json(data['map_size'])
        self.locations: dict[tuple[Vector]:list[GameObject]] = {
            tuple(map(lambda vec: Vector().from_json(vec), k)): [self.__from_json_helper(obj) for obj in v] for k, v in
            zip(data["location_vectors"], data["location_objects"])} if data["location_vectors"] is not None else None
        self.walled: bool = data["walled"]
        self.event_active: int = data['event_active']
        self.game_map: list[list[Tile]] = [
            [Tile().from_json(tile) for tile in y] for y in temp] if temp is not None else None
        self.inventory_manager: InventoryManager = InventoryManager().from_json(data['inventory_manager'])
        self.church_trap_queue: TrapQueue = TrapQueue().from_json(data['church_trap_queue'])
        self.turing_trap_queue: TrapQueue = TrapQueue().from_json(data['turing_trap_queue'])
        self.dynamite_list = DynamiteList().from_json(data['dynamite_list'])
        return self

    def trap_detonation_control(self):
        self.church_trap_queue.detonate(self.inventory_manager)
        self.turing_trap_queue.detonate(self.inventory_manager)

    def dynamite_detonation_control(self):
        self.dynamite_list.detonate(self.inventory_manager)
