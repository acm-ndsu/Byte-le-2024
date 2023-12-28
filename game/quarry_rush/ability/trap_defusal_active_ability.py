from game.quarry_rush.ability.active_ability import ActiveAbility
from game.common.enums import ObjectType


class TrapDefusalActiveAbility(ActiveAbility):
    def __init__(self, cooldown: int = 0, fuse: int = 0):
        super().__init__()
        self.object_type = ObjectType.TRAP_DEFUSAL_ACTIVE_ABILITY
        self.cooldown = cooldown  # default = 0 to always be available
        self.fuse = fuse  # default = 0 to be available right after purchase
