from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from typing import Self


class Avatar(GameObject):
    def __init__(self, item: Item = None, position: tuple[int,int]=None):
        super().__init__()
        self.object_type = ObjectType.AVATAR
        self.held_item = item
        self.score = 0
        self.position = position

    @property
    def held_item(self) -> Item:
        return self.__held_item

    @property
    def score(self) -> int:
        return self.__score

    @property
    # return format for tuple (x-position, y-position), assumes (0,0) is top left of the game board
    def position(self) -> tuple[int, int]:
        return self.__position

    @held_item.setter
    def held_item(self, item: Item):
        # If it's not an item, and it's not None, raise the error
        if not isinstance(item, Item) and item:
            raise ValueError("avatar.held_item must be an Item or None.")
        self.__held_item = item

    @score.setter
    def score(self, score: int):
        if not isinstance(score, int):
            raise ValueError("avatar.score must be an int.")
        self.__score = score

    @position.setter
    def position(self, position: tuple[int, int]):
        if not(isinstance(position, tuple) and list(map(type, position)) == [int, int]) and position:
            raise ValueError("avatar.position must be a tuple of two ints.")
        self.__position = position

    def to_json(self) -> dict:
        data = super().to_json()
        data['held_item'] = self.held_item.to_json() if self.held_item else None
        data['score'] = self.score
        data['position'] = self.position
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.score = data['score']
        self.position = data['position']
        temp: Item = data['held_item']
        if temp is None:
            self.held_item = None
        elif temp.object_type == ObjectType.ITEM:
            self.held_item = Item().from_json(data['held_item'])
        else:
            raise ValueError("avatar.held_item needs to be an item.")
        return self
