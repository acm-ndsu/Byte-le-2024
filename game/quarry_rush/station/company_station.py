from game.common.stations.occupiable_station import OccupiableStation
from game.common.avatar import Avatar
from game.common.enums import Company
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.common.enums import ObjectType
from typing import Self


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
            inventory_manager.cash_in_all(self.company)

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['company'] = self.company.value
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.company: Company = Company(data['company'])
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
