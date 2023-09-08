from game.common.items.item import Item
from game.utils.vector import Vector
from game.common.enums import Company
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from typing import Self
from typing import Callable


class Trap(Item):
    """
    Class inheriting the Item class that is the generic for traps placed on the game_board
    Added values:   detection_reduction, steal_rate, inventory_manager, owner_company, target_company, opponent_position
    Added methods:
        - in_range: checks if opponent_position is within range of the trap
        - detonate: if in_range returns true, then detonate the trap, stealing from the opposing avatar
                    with a method from inventory_manager class. game_board will check if detonate == true, 
                    if so, remove trap from game_board trap queue to remove it from the game.
    """

    def __init__(self, detection_reduction: float = 0.0, steal_rate: float = 0.0,
                 owner_company: Company = Company.CHURCH, target_company: Company = Company.TURING,
                 opponent_position: Callable[[], Vector] = lambda: Vector(), position: Vector = Vector()):
        super().__init__(position=position)
        # value subtracting from default 5% detection rate
        self.detection_reduction: float = detection_reduction
        # rate for stealing items from opposing avatar when trap detonates (if none, pass 0.0)
        self.steal_rate: float = steal_rate
        # company of the owner of the trap
        self.owner_company: Company = owner_company
        # company of the target
        self.target_company: Company = target_company
        # function that returns Vector of opponent position
        self.opponent_position: Callable[[], Vector] = opponent_position

    # getter methods
    @property
    def detection_reduction(self) -> float:
        return self.__detection_reduction

    @property
    def steal_rate(self) -> float:
        return self.__steal_rate

    @property
    def owner_company(self) -> Company:
        return self.__owner_company

    @property
    def target_company(self) -> Company:
        return self.__target_company

    @property
    def opponent_position(self) -> Callable[[], Vector]:
        return self.__opponent_position

    # setter methods
    @detection_reduction.setter
    def detection_reduction(self, detection_reduction: float) -> None:
        if detection_reduction is None or not isinstance(detection_reduction, float):
            raise ValueError(
                f'{self.__class__.__name__}.detection_reduction must be a float.')
        self.__detection_reduction = detection_reduction

    @steal_rate.setter
    def steal_rate(self, steal_rate: float) -> None:
        if steal_rate is None or not isinstance(steal_rate, float):
            raise ValueError(
                f'{self.__class__.__name__}.steal_rate must be a float.')
        self.__steal_rate = steal_rate

    @opponent_position.setter
    def opponent_position(self, opponent_position: Callable[[], Vector]) -> None:
        try:
            if not isinstance(opponent_position(), Vector):
                raise Exception
        except:
            raise ValueError(
                f'{self.__class__.__name__}.opponent_position must be of type Callable[[], Vector].'
            )

        self.__opponent_position = opponent_position

    @owner_company.setter
    def owner_company(self, owner_company: Company) -> None:
        if owner_company is None or not isinstance(owner_company, Company):
            raise ValueError(
                f'{self.__class__.__name__}.owner_company must be of enum type Company.')
        self.__owner_company = owner_company

    @target_company.setter
    def target_company(self, target_company: Company) -> None:
        if target_company is None or not isinstance(target_company, Company):
            raise ValueError(
                f'{self.__class__.__name__}.target_company must be of enum type Company.')
        self.__target_company = target_company

    # in_range method, checks to see if opposing player is in range of detonating a trap
    def in_range(self) -> bool:
        # find distance between trap position and opponent_position using method from vector class
        # if distance is less than or equal to maximum distance, then return True, else, False
        opponent_position = self.opponent_position()
        if Vector.distance(self.position, opponent_position) <= 1:
            return True
        return False

    # detonation method, calls in_range and steal to detonate trap
    def detonate(self, inventory_manager: InventoryManager) -> bool:
        # check if opposing player is in range with in_range method
        # if in_range returns True, run rest of method
        # use steal method from inventory_manager class
        # will be removed by game_board if returns True
        if self.in_range() == True:
            inventory_manager.steal(self.owner_company, self.target_company, self.steal_rate)
            return True
        return False

    # json methods
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['detection_reduction'] = self.detection_reduction
        data['steal_rate'] = self.steal_rate
        data['owner_company'] = self.owner_company
        data['target_company'] = self.target_company
        data['opponent_position'] = self.opponent_position
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.detection_reduction: float = data['detection_reduction']
        self.steal_rate: float = data['steal_rate']
        self.owner_company: Company = data['owner_company']
        self.target_company: Company = data['target_company']
        self.opponent_position: Callable[[], Vector] = data['opponent_position']
        return self


# default classes for Landmine and EMP with existing detection_reduction and steal_rate

class Landmine(Trap):

    def __init__(self, owner_company: Company, target_company: Company,
                 opponent_position: Callable[[], Vector], position: Vector):
        super().__init__(0.0, 0.1, owner_company, target_company, opponent_position, position)


class EMP(Trap):

    def __init__(self, owner_company: Company, target_company: Company,
                 opponent_position: Callable[[], Vector], position: Vector):
        super().__init__(0.1, 0.2, owner_company, target_company, opponent_position, position)
