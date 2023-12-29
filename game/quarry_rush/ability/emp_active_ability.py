from game.quarry_rush.ability.active_ability import ActiveAbility
from game.common.enums import ObjectType


class EMPActiveAbility(ActiveAbility):

    def __init__(self, cooldown: int = 4, fuse: int = 0):
        super().__init__()
        self.object_type: ObjectType = ObjectType.EMP_ACTIVE_ABILITY
        self.cooldown: int = cooldown
        self.fuse: int = fuse  # default = 0 to be available right after purchase
