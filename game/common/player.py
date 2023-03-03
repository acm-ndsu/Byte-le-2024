from game.common.action import Action
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.enums import *


class Player(GameObject):
    def __init__(self, code: object = None, team_name: str = None, action: Action = None, avatar: Avatar = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.PLAYER
        self.functional: bool = True
        self.error: object = None
        self.team_name: str = team_name
        self.code: object = code
        self.action: Action = action
        self.avatar: Avatar = avatar

    @property
    def action(self) -> Action:  # Will need to change Avatar class to the enum eventually
        return self.__action

    @action.setter
    def action(self, action: Action):
        if action is None or isinstance(action, Action):
            self.__action = action

    @property
    def functional(self) -> bool:
        return self.__functional

    @functional.setter
    def functional(self, functional: bool):
        if functional is None or isinstance(functional, bool):
            self.__functional = functional

    @property
    def team_name(self) -> str:
        return self.__team_name

    @team_name.setter
    def team_name(self, team_name: str):
        if team_name is None or isinstance(team_name, str):
            self.__team_name = team_name

    @property
    def avatar(self) -> Avatar:
        return self.__avatar

    @avatar.setter
    def avatar(self, avatar: Avatar):
        if avatar is None or isinstance(avatar, Avatar):
            self.__avatar = avatar

    @property
    def object_type(self) -> ObjectType:
        return self.object_type

    @object_type.setter
    def object_type(self, object_type: ObjectType):
        if object_type is None or isinstance(object_type, GameObject):
            self.__object_type = object_type

    def to_json(self):
        data = super().to_json()

        data['functional'] = self.functional
        data['error'] = self.error
        data['team_name'] = self.team_name
        data['action'] = self.action.to_json() if self.action is not None else None
        data['avatar'] = self.avatar.to_json() if self.avatar is not None else None

        return data

    def from_json(self, data):
        super().from_json(data)
        
        self.functional = data['functional']
        self.error = data['error']
        self.team_name = data['team_name']
        self.action = Action().from_json(data['action']) if data['action'] is not None else None
        self.avatar = Avatar().from_json(data['avatar']) if data['avatar'] is not None else None

    def __str__(self):
        p = f"""ID: {self.id}
            Team name: {self.team_name}
            Action: {self.action}
            """
        return p
