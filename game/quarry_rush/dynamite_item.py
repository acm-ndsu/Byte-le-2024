from game.utils.vector import Vector
from game.common.items.item import Item
from game.common.avatar import Avatar


class DynamiteItem(Item):
    def __init__(self, value: int = 1, durability: int | None = None, quantity: int = 1, stack_size: int = 1,
                 position: Vector | None = None, name: str | None = None, blast_radius: int = 1,
                 avatar: Avatar | None = None, detonate_turn: int = 1):
        super().__init__()
        self.value: int = value
        self.__durability = None
        self.durability: int | None = durability
        self.__quantity = None
        self.quantity: int = quantity
        self.stack_size: int = stack_size
        self.position: Vector | None = position
        self.name: str | None = name
        self.blast_radius: int = blast_radius
        self.avatar: Avatar | None = avatar
        self.detonate_turn: int = detonate_turn

    # value getter
    @property
    def value(self) -> int:
        return self.__value

    # value setter
    @value.setter
    def value(self, value: int) -> None:
        if value is None or not isinstance(value, int):
            raise ValueError(f'{self.__class__.__name__}.value must be an int')
        self.__value = value

    # durability getter
    @property
    def durability(self) -> int | None:
        return self.__durability

    # durability setter
    @durability.setter
    def durability(self, durability: int | None) -> None:
        if durability is not None and not isinstance(durability, int):
            raise ValueError(f'{self.__class__.__name__}.durability must be an int or None.')
        if durability is not None and self.stack_size != 1:
            raise ValueError(
                f'{self.__class__.__name__}.durability must be set to None if stack_size is not equal to 1.')
        self.__durability = durability

    # quantity getter
    @property
    def quantity(self) -> int:
        return self.__quantity

    # quantity setter
    @quantity.setter
    def quantity(self, quantity: int) -> None:
        if quantity is None or not isinstance(quantity, int):
            raise ValueError(f'{self.__class__.__name__}.quantity must be an int.')
        if quantity < 0:
            raise ValueError(f'{self.__class__.__name__}.quantity must be greater than or equal to 0.')

        # The self.quantity is set to the lower value between stack_size and the given quantity
        # The remaining given quantity is returned if it's larger than self.quantity
        if quantity > self.stack_size:
            raise ValueError(f'{self.__class__.__name__}.quantity cannot be greater than '
                             f'{self.__class__.__name__}.stack_size')
        self.__quantity: int = quantity

    # stack size getter
    @property
    def stack_size(self) -> int:
        return self.__stack_size

    # stack size setter
    @stack_size.setter
    def stack_size(self, stack_size: int) -> None:
        if stack_size is None or not isinstance(stack_size, int):
            raise ValueError(f'{self.__class__.__name__}.stack_size must be an int.')
        if self.durability is not None and stack_size != 1:
            raise ValueError(f'{self.__class__.__name__}.stack_size must be 1 if {self.__class__.__name__}.durability '
                             f'is not None.')
        if self.__quantity is not None and stack_size < self.__quantity:
            raise ValueError(f'{self.__class__.__name__}.stack_size must be greater than or equal to the quantity.')
        self.__stack_size: int = stack_size

    # position getter
    @property
    def position(self) -> Vector | None:
        return self.__position

    # position setter
    @position.setter
    def position(self, position: Vector | None) -> None:
        if position is not None and not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector or None.')
        self.__position: Vector | None = position

    # name getter
    @property
    def name(self) -> str | None:
        return self.__name

    # name setter
    @name.setter
    def name(self, name: str | None) -> None:
        if name is not None and not isinstance(name, str):
            raise ValueError(f'{self.__class__.__name__}.name must be a str or None.')
        self.__name: str | None = name

    # blast radius getter
    @property
    def blast_radius(self) -> int:
        return self.__blast_radius

    # blast radius setter
    @blast_radius.setter
    def blast_radius(self, blast_radius: int) -> None:
        if blast_radius is None or not isinstance(blast_radius, int):
            raise ValueError(f'{self.__class__.__name__}.blast_radius must be an int.')
        self.__blast_radius: int = blast_radius

    # avatar getter
    @property
    def avatar(self) -> Avatar:
        return self.__avatar

    # avatar setter
    @avatar.setter
    def avatar(self, avatar: Avatar) -> None:
        if avatar is not None and not isinstance(avatar, Avatar):
            raise ValueError(f'{self.__class__.__name__}.avatar must be Avatar or None')
        self.__avatar = avatar

    # detonate_turn getter
    @property
    def detonate_turn(self) -> int:
        return self.__detonate_turn

    # detonate_turn setter
    @detonate_turn.setter
    def detonate_turn(self, detonate_turn: int) -> None:
        if detonate_turn is None or not isinstance(detonate_turn, int):
            raise ValueError(f'{self.__class__.__name__}.blast_radius must be an int')
        self.__detonate_turn = detonate_turn

    # detonate method

    # explode dynamite
    def explode(self):



