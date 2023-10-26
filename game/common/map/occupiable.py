from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from typing import Self


class Occupiable(GameObject):
    """
    `Occupiable Class Notes:`

        Occupiable objects exist to encapsulate all objects that could be placed on the gameboard.

        These objects can only be occupied by GameObjects, so inheritance is important. The ``None`` value is
        acceptable for this too, showing that nothing is occupying the object.

        Note: The class Item inherits from GameObject, but it is not allowed to be on an Occupiable object.
    """

    def __init__(self, occupied_by: GameObject = None, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.OCCUPIABLE
        self.occupied_by: GameObject | None = occupied_by

    @property
    def occupied_by(self) -> GameObject | None:
        return self.__occupied_by

    @occupied_by.setter
    def occupied_by(self, occupied_by: GameObject | None) -> None:
        if occupied_by is not None and isinstance(occupied_by, Item):
            raise ValueError(f'{self.__class__.__name__}.occupied_by cannot be an Item.')
        if occupied_by is not None and not isinstance(occupied_by, GameObject):
            raise ValueError(f'{self.__class__.__name__}.occupied_by must be None or an instance of GameObject.')
        self.__occupied_by = occupied_by

    def place_on_top_of_stack(self, game_object: GameObject) -> bool:
        """
        This method will take in a GameObject and place it on top of the occupied_by stack of the Occupiable object.
        """
        temp_game_object: Self = self

        # Execute loop only if the object occupying self is an object (i.e., not none) and can also be occupied
        while temp_game_object.occupied_by is not None and hasattr(temp_game_object.occupied_by, 'occupied_by'):
            # moves to the next thing in the stack of occupiable objects
            temp_game_object = temp_game_object.occupied_by

        if temp_game_object.occupied_by is not None:
            if not isinstance(temp_game_object.occupied_by, Avatar) or not hasattr(game_object, 'occupied_by'):
                return False

            game_object.occupied_by = temp_game_object.occupied_by

        temp_game_object.occupied_by = game_object  # assign the last thing on top of the stack that is occupiable

        return True

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['occupied_by'] = self.occupied_by.to_json() if self.occupied_by is not None else None
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        return self
