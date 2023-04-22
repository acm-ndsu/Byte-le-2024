from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.common.items.item import Item
from typing import Self


# create Station object from GameObject that allows item to be contained in it
class Station(GameObject):
    """
    A Station is an Object that inherits from GameObject. Stations are able to contain Items in them. Players can
    interact with Stations to receive the items. (Refer to avatar.py and item.py to see how this works).
    """

    def __init__(self, held_item: Item | None = None, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.STATION
        self.held_item: Item | None = held_item

    # held_item getter and setter methods
    @property
    def held_item(self) -> Item | None:
        return self.__item

    @held_item.setter
    def held_item(self, held_item: Item) -> None:
        if held_item is not None and not isinstance(held_item, Item):
            raise ValueError(f'{self.__class__.__name__}.held_item must be an Item or None, not {held_item}.')
        self.__item = held_item

    # take action method
    def take_action(self, avatar: Avatar) -> Item | None:
        return self.held_item

    # json methods
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['held_item'] = self.held_item.to_json() if self.held_item is not None else None

        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        held_item: dict = data['held_item']
        if held_item is None:
            self.held_item = None
            return self

        # framework match case for from json, can add more object types that can be item
        match held_item['object_type']:
            case ObjectType.ITEM:
                self.held_item = Item().from_json(data['held_item'])
            case _:
                raise Exception(f'Could not parse held_item: {self.held_item}')
        return self
