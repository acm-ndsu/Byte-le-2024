from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base
from .timestamp import TimeStamp


class Tournament(Base):
    """
    'Tournament' Model Class - Shapes the 'tournament' table in the database
    tournament_id: primary key
    start_run
    launcher_version
    runs_per_client
    is_finished

    Related table:
        * runs
    """

    # Date times are stored in UTC in ISO format
    __tablename__: str = 'tournament'
    tournament_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    start_run: Mapped[str] = mapped_column(TimeStamp(), nullable=False)
    launcher_version: Mapped[str] = mapped_column(String(10), nullable=False)
    runs_per_client: Mapped[int] = mapped_column(Integer(), nullable=False)
    is_finished: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)

    runs: Mapped[list['Run']] = relationship(back_populates='tournament', passive_deletes=True)

