from game.common.items.item import Item
from game.common.avatar import Avatar
from game.utils.vector import Vector
from typing import Self

class Trap(Item):

    """
    Class inheriting the Item class that is the generic for traps placed on the game_board
    Added values:   activated, detection_reduction, steal_rate, owner
    Added methods:
        - in_range: checks if an avatar that is not the owner is within range of the trap
        - detonate: if in_range returns true, then detonate the trap, stealing from the opposing avatar and removing the trap from the game_board
    """
    def __init__(self, activated: bool, detection_reduction: float, steal_rate: float, owner: Avatar, value: int = 1, durability: int | None = None, quantity: int = 1, stack_size: int = 1, position: Vector | None = None, name: str | None = None):
        super().__init__(value, durability, quantity, stack_size, position, name)
        self.activated: bool = activated                    # sees if trap has been activated
        self.detection_reduction = detection_reduction      # value subtracting from default 5% detection rate
        self.steal_rate: float = steal_rate                 # rate for stealing items from opposing avatar when trap detonates (if none, pass 0)
        self.owner: Avatar = owner                          # owner of trap (value passed should be the player's avatar that placed the trap)
        self.add_queue()                                    # adds trap to the owner's queue


    # getter methods
    @property
    def activated(self) -> bool:
        return self.__activated
    
    @property
    def detection_reduction(self) -> float:
        return self.__detection_reduction
    
    @property
    def steal_rate(self) -> float:
        return self.__steal_rate
    
    @property
    def owner(self) -> Avatar:
        return self.__owner
    
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

    @steal_rate.setter
    def steal_rate(self, steal_rate: float) -> None:
        if steal_rate is None or not isinstance(steal_rate, float):
            raise ValueError(f'{self.__class__.__name__}.steal_rate must be a float.')
        self.__steal_rate = steal_rate
        
    @owner.setter
    def owner(self, owner: Avatar) -> None:
        if owner is None or not isinstance(owner, Avatar):
            raise ValueError(f'{self.__class__.__name__}.owner must be of type Avatar.')
        self.__owner = owner

    # add_queue method, adds trap to a queue stored on the owner, which is rendered onto the game_board
    def add_queue(self) -> None:
        # call enqueue method on queue of owner to add trap to owner's queue
        # if queue is too large, dequeue first item in queue to remove it from game_board and add new one
        pass

    # in_range method, checks to see if opposing player is in range of detonating a trap
    def in_range(self) -> bool:
        # find distance between trap position and target position
        # if distance is less than or equal to maximum distance, then return true, else, false
        pass

    # detonation method, implemented in specific traps
    def detonate(self) -> None:
        # check if opposing player is in range with in_range method which uses distance calc in vector class
        # if activated is now true, run rest of method
        # use steal method
        # will remove itself with a method in the avatar class using trap queues
        pass

    # json methods
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['activated'] = self.activated
        data['detection_reduction'] = self.detection_reduction
        data['steal_rate'] = self.steal_rate
        data['owner'] = self.owner.to_json()
        return data
    
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.activated: bool = data['activated']
        self.detection_reduction: float = data['detection_reduction']
        self.steal_rate: float = data['steal_rate']
        self.owner: Avatar = Avatar().from_json(data['owner'])
        return self