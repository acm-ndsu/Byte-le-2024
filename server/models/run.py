from sqlalchemy import LargeBinary, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Run(Base):
    __tablename__: str = 'run'
    run_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    group_run_id: Mapped[int] = mapped_column(Integer(), ForeignKey("group_run.group_run_id"))
    run_time: Mapped[str] = mapped_column(DateTime(), nullable=False)
    winner: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    player_1: Mapped[int] = mapped_column(Integer(), nullable=False)
    player_2: Mapped[int] = mapped_column(Integer(), nullable=False)
    seed: Mapped[int] = mapped_column(Integer(), nullable=False)

    # results is a JSON file that's read in, so it needs to be a LargeBinary object.
    results: Mapped[str] = mapped_column(LargeBinary(), nullable=False)
