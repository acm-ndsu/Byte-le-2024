from __future__ import annotations

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
        temp_game_object: GameObject = self

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

    def is_occupied_by(self, object_type: ObjectType) -> bool:
        """
        This method searches for the given ObjectType in the stack of occupied_by. If found, it returns that object;
        None is returned otherwise.
        """

        # start on the first object in the stack that isn't this object
        temp_game_object: GameObject = self.occupied_by

        # only check if the object is None because we want to look through the entire stack of objects.
        while temp_game_object is not None:

            # if the object is what we want, return true
            if temp_game_object.object_type == object_type:
                return True

            if hasattr(temp_game_object, 'occupied_by'):
                # moves to the next thing in the stack of occupiable objects
                temp_game_object = temp_game_object.occupied_by
            else:
                return False  # if the object doesn't have the attribute, wanted object isn't in stack

        # if the wanted object isn't found, return False
        return False

    def get_occupied_by(self, target: ObjectType | GameObject) -> GameObject | None:
        """
        Get the object in the occupied_by stack given either the ObjectType or GameObject. Returns the GameObject in
        the stack, but None if it isn't there.
        """
        # start on the first object in the stack that isn't this object
        temp_game_object: GameObject = self.occupied_by
        while temp_game_object is not None:
            if (isinstance(target, ObjectType) and temp_game_object.object_type == target) or \
                    isinstance(target, GameObject) and isinstance(temp_game_object, target.__class__):
                return temp_game_object

            if isinstance(temp_game_object, Occupiable):
                temp_game_object = temp_game_object.occupied_by
            else:
                return None

        return temp_game_object

    def remove_from_occupied_by(self, object_type: ObjectType | None = None) -> GameObject | None:
        """
        This method will remove the first instance of the given ObjectType found in the occupied by stack.
        """

        # if the object type isn't in the stack, return None
        if not self.is_occupied_by(object_type):
            return None

        current_game_object: GameObject = self

        # variable to store what the next thing in the stack is. Either None or a GameObject
        next_game_object: GameObject = current_game_object.occupied_by

        while (current_game_object and next_game_object is not None) and \
                current_game_object.occupied_by.object_type != object_type:
            current_game_object = current_game_object.occupied_by
            next_game_object = next_game_object.occupied_by

        # at top of stack without finding wanted object
        if next_game_object is None:
            return None

        if next_game_object.object_type == object_type:
            # reassign the current game_object's occupied_by and return what the next game object is
            current_game_object.occupied_by = next_game_object.occupied_by
            return next_game_object

        return None

        # make references of the objects in the stack
        # prev_game_object: GameObject = self  # used to keep track of reconnecting the stack after removing an object
        #
        # # the current is the occupied_by object to ensure we can have a previous and next object
        # current_game_object: GameObject = self.occupied_by
        #
        # next_game_object: GameObject = self.occupied_by.occupied_by  # used to reference the next object in the stack
        #
        # # loop only when the current and next objects are not None and the current object type doesn't match the given
        # while (current_game_object and next_game_object is not None) and current_game_object.object_type != object_type:
        #     # shift all objects up the stack
        #     prev_game_object = current_game_object
        #     current_game_object = next_game_object
        #     next_game_object = next_game_object.occupied_by
        #
        # if next_game_object is None and current_game_object is not None:
        #     return current_game_object
        #
        # # reorder the occupied_by stack
        # prev_game_object.occupied_by = next_game_object
        #
        # # return what was removed
        # return current_game_object




    # def find_occupied_by(self, object_type: ObjectType | None = None, game_object: GameObject | None = None) -> \
    #         GameObject | None:
    #     """
    #     This method takes a ObjectType and checks if this Occupiable object is occupied by it. If so, it returns the
    #     object in the stack. If not, it returns None
    #     """
    #
    #     # start on the first thing in the stack that isn't this object
    #     temp_game_object: GameObject = self.occupied_by
    #
    #     print(f'FIRST OCCUPIED BY: {temp_game_object.object_type}')  # DELETE AFTER TESTS
    #
    #     while isinstance(temp_game_object, Occupiable) and temp_game_object.occupied_by is not None:
    #         if temp_game_object.object_type == object_type or (game_object is not None and
    #                                                            isinstance(temp_game_object, game_object.__class__)):
    #             return temp_game_object  # return the object looked for
    #
    #         # checks that the game object is still an Occupiable for the while loop condition
    #         if not isinstance(temp_game_object, Occupiable):
    #             return None
    #
    #         # moves to the next thing in the stack of occupiable objects
    #         temp_game_object = temp_game_object.occupied_by
    #
    #         print(f'NEXT OCCUPIED BY: {temp_game_object.object_type}')  # DELETE AFTER TESTS
    #
    #     return None

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['occupied_by'] = self.occupied_by.to_json() if self.occupied_by is not None else None
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        return self
