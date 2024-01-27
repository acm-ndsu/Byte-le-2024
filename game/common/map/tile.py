from typing import Self

from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
from game.common.map.wall import Wall
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.traps import EMP, Landmine
from game.quarry_rush.station.company_station import ChurchStation, TuringStation


class Tile(Occupiable):
    """
    `Tile Class Notes:`

        The Tile class exists to encapsulate all objects that could be placed on the gameboard.

        Tiles will represent things like the floor in the game. They inherit from Occupiable, which allows for tiles to
        have certain GameObjects and the avatar on it.

        If the game being developed requires different tiles with special properties, future classes may be added and
        inherit from this class.
    """

    def __init__(self, occupied_by: GameObject = None):
        super().__init__(occupied_by)
        self.object_type: ObjectType = ObjectType.TILE

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        occupied_by: dict | None = data['occupied_by']
        if occupied_by is None:
            self.occupied_by = None
            return self
        # Add all possible game objects that can occupy a tile here (requires python 3.10) 
        match ObjectType(occupied_by['object_type']):
            case ObjectType.AVATAR:
                self.occupied_by: Avatar = Avatar().from_json(occupied_by)
            case ObjectType.OCCUPIABLE_STATION:
                self.occupied_by: OccupiableStation = OccupiableStation().from_json(occupied_by)
            case ObjectType.ORE_OCCUPIABLE_STATION:
                # I know it's bad practice, but it's to prevent a circular import
                from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation
                self.occupied_by: OreOccupiableStation = OreOccupiableStation().from_json(occupied_by)
            case ObjectType.STATION:
                self.occupied_by: Station = Station().from_json(occupied_by)
            case ObjectType.WALL:
                self.occupied_by: Wall = Wall().from_json(occupied_by)
            case ObjectType.CHURCH_STATION:
                self.occupied_by: ChurchStation = ChurchStation().from_json(occupied_by)
            case ObjectType.TURING_STATION:
                self.occupied_by: TuringStation = TuringStation().from_json(occupied_by)
            case ObjectType.DYNAMITE:
                self.occupied_by: Dynamite = Dynamite().from_json(occupied_by)
            case ObjectType.LANDMINE:
                self.occupied_by: Landmine = Landmine().from_json(occupied_by)
            case ObjectType.EMP:
                self.occupied_by: EMP = EMP().from_json(occupied_by)
            case _:
                raise ValueError(f'Could not parse occupied_by: {occupied_by}')
        return self
