from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base
from uuid import uuid4


class Team(Base):
    __tablename__: str = 'team'
    team_id_uuid: Mapped[int] = mapped_column(Integer(), primary_key=True, default=uuid4())
    uni_id: Mapped[int] = mapped_column(Integer(), ForeignKey("university.uni_id"))
    team_type_id: Mapped[int] = mapped_column(Integer(), ForeignKey("team_type.team_type_id"))
    team_name: Mapped[str] = mapped_column(String(), CheckConstraint("team_name != ''"), unique=True, nullable=False)
