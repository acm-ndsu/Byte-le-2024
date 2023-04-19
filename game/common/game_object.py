import uuid

from game.common.enums import ObjectType
from typing import Self


class GameObject:
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.object_type = ObjectType.NONE

    def to_json(self) -> dict:
        # It is recommended call this using super() in child implementations
        data = dict()

        data['id'] = self.id
        data['object_type'] = self.object_type

        return data

    def from_json(self, data: dict) -> Self:
        # It is recommended call this using super() in child implementations
        self.id = data['id']
        self.object_type = data['object_type']
        return self

    def obfuscate(self):
        pass
