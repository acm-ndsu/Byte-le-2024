from game.common.items.item import Item
from game.utils.vector import Vector

class Trap(Item):

    """
    Class inheriting the Item class that is the generic for traps placed on the game_board
    Added values:   activated, detection_reduction
    """
    def __init__(self, activated: bool, detection_reduction: float, value: int = 1, durability: int | None = None, quantity: int = 1, stack_size: int = 1, position: Vector | None = None, name: str | None = None):
        super().__init__(value, durability, quantity, stack_size, position, name)
        self.activated = activated                          # sees if trap has been activated
        self.detection_reduction = detection_reduction      # value subtracting from default 5% detection rate

    # getter methods
    @property
    def activated(self) -> bool:
        return self.__activated
    
    @property
    def detection_reduction(self) -> float:
        return self.__detection_reduction
    
    # setter methods
    @activated.setter
    def activated(self, activated: bool) -> None:
        if activated is None or not isinstance(activated, bool):
            raise ValueError(f'{self.__class__.__name__}.activated must be a bool.')
        self.__activated = activated

    @detection_reduction.setter
    def detection_reduction(self, detection_reduction: float) -> None:
        if detection_reduction is None or not isinstance(detection_reduction, float):
            raise ValueError(f'{self.__class__.__name__}.detection_reduction must be a float.')
        self.__detection_reduction = detection_reduction

    # in_range method, checks to see if opposing player is in range of detonating a trap


    # detonation method, implemented in specific traps
    def detonate(self) -> None:
        # check if opposing player is in range with in_range method which uses distance calc in vector class
        # if activated is now true, run rest of method
        # use steal method
        # will remove itself with a method in the avatar class using trap queues
        pass

    # json methods
