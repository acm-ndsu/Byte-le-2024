from sqlalchemy import Integer, Boolean, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TeamType(Base):
    __tablename__: str = 'team_type'
    team_type_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    team_type_name: Mapped[str] = mapped_column(String(15), CheckConstraint("team_type_name != ''"), nullable=False,
                                                unique=True)
    eligible: Mapped[bool] = mapped_column(Boolean(), nullable=False)
