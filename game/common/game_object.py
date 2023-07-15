import uuid

from game.common.enums import ObjectType
from typing import Self


class GameObject:
    """
    This class is widely used throughout the project to represent different types of Objects that are interacted
    with in the game.
    """
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.object_type = ObjectType.NONE
        self.state = "idle"

    def to_json(self) -> dict:
        # It is recommended call this using super() in child implementations
        data = dict()

        data['id'] = self.id
        data['object_type'] = self.object_type.value
        data['state'] = self.state

        return data

    def from_json(self, data: dict) -> Self:
        # It is recommended call this using super() in child implementations
        self.id = data['id']
        self.object_type = ObjectType(data['object_type'])
        self.state = data['state']
        return self

    def obfuscate(self):
        pass
