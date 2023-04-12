from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.common.items.item import Item
from typing import Self

# create Station object from GameObject that allows item to be contained in it
class Station(GameObject):
    def __init__(self, item: Item|None = None, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.STATION
        self.item: Item|None = item

    # item getter and setter methods
    @property
    def item(self) -> Item|None:
        return self.__item

    @item.setter
    def item(self, item: Item) -> None:
        if item is not None and not isinstance(item, Item):
            raise ValueError(f"{self.__class__.__name__}.item must be an Item or None, not {item}.")
        self.__item = item

    # take action method
    def take_action(self, avatar: Avatar) -> Item|None:
        return

    # json methods
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['item'] = self.item.to_json() if self.item is not None else None

        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        item: dict = data['item']
        if item is None:
            self.item = None
            return self

        # framework match case for from json, can add more object types that can be item
        match item['object_type']:
            case ObjectType.ITEM:
                self.item = Item().from_json(data['item'])
            case _:
                raise Exception(f'Could not parse item: {self.item}')   

        return self
    