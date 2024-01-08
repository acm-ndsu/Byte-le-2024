from sqlalchemy import Integer, Boolean, CheckConstraint, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class TeamType(Base):
    """
    'Team Type' Model Class - Shapes the 'team_type' table in the database
    team_type_id: primary key
    team_type_name: must be unique - uniqueness prevents confusion when giving prizes at end of competition
    eligible

    Related table:
        * teams
    """

    __tablename__: str = 'team_type'
    team_type_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    team_type_name: Mapped[str] = mapped_column(String(15), CheckConstraint("team_type_name != ''"), nullable=False,
                                                unique=True)
    eligible: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    teams: Mapped[list['Team']] = relationship(back_populates='team_type')
