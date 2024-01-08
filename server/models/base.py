from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    This class is needed to create all the database tables and establish the database session. This is why it's
    inherited in all base classes in the ``models`` folder. All models inherit from ``DeclarativeBase``, so
    this helps simplify the inheritance and import slightly.
    """
    pass
