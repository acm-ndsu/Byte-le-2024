from sqlalchemy import Integer, CheckConstraint, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class University(Base):
    """
    'University' Model Class - Shapes the 'university' table in the database
    uni_id: primary key
    uni_name: must be unique

    Related table:
        * team
    """

    __tablename__: str = 'university'

    uni_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    uni_name: Mapped[str] = mapped_column(String(100), CheckConstraint("uni_name != ''"), nullable=False, unique=True)

    teams: Mapped[list['Team']] = relationship(back_populates='university')
