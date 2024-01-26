from game.common.stations.occupiable_station import OccupiableStation
from game.common.avatar import Avatar
from game.common.enums import Company
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.common.enums import ObjectType
from typing import Self

from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.traps import Landmine, EMP


class CompanyStation(OccupiableStation):
    """
    CompanyStation is a station inheriting from OccupiableStation

    This station contains a company which correlates to the avatar's company.
    These stations are auto-generated in game_location.py

    take_action: if the avatar's company matches the company of the station, the avatar can
    run cash_in_all
    """

    def __init__(self, company: Company):
        super().__init__()
        self.company: Company = company
        self.object_type = ObjectType.COMPANY_STATION

    # company getter and setter methods
    @property
    def company(self) -> Company:
        return self.__company

    @company.setter
    def company(self, company: Company) -> None:
        if company is None or not isinstance(company, Company):
            raise ValueError(f'{self.__class__.__name__}.company must be a Company.')
        self.__company = company

    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager) -> None:
        if avatar.company == self.company:
            points, science = inventory_manager.cash_in_all(self.company)
            avatar.score += points
            avatar.science_points += science

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['company'] = self.company.value
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.company: Company = Company(data['company'])
        if self.occupied_by is not None:
            return self
        occupied_by = data['occupied_by']
        if occupied_by is None:
            self.occupied_by = None
            return self
        # Add all possible game objects that can occupy a tile here (requires python 3.10)
        match ObjectType(occupied_by['object_type']):
            case ObjectType.DYNAMITE:
                self.occupied_by: Dynamite = Dynamite().from_json(occupied_by)
            case ObjectType.LANDMINE:
                self.occupied_by: Landmine = Landmine().from_json(occupied_by)
            case ObjectType.EMP:
                self.occupied_by: EMP = EMP().from_json(occupied_by)
            case _:
                raise Exception(f'Could not parse occupied_by: {occupied_by}')
        return self


class ChurchStation(CompanyStation):
    """
    Class to generate base stations for Church.
    """
    def __init__(self):
        super().__init__(Company.CHURCH)
        self.object_type = ObjectType.CHURCH_STATION


class TuringStation(CompanyStation):
    """
    Class to generate base stations for Turing.
    """
    def __init__(self):
        super().__init__(Company.TURING)
        self.object_type = ObjectType.TURING_STATION
