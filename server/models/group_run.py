from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base
from .run import Run


class GroupRun(Base):
    # Date times are stored in UTC in ISO format
    __tablename__: str = 'group_run'
    group_run_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    start_run: Mapped[str] = mapped_column(DateTime(), nullable=False)
    launcher_version: Mapped[str] = mapped_column(String(10), nullable=False)
    runs_per_client: Mapped[int] = mapped_column(Integer(), nullable=False)
    is_finished: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    runs: Mapped[list[Run]] = relationship()
