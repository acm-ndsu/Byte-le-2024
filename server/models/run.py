from sqlalchemy import LargeBinary, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .timestamp import TimeStamp


class Run(Base):
    """
    Run Model Class - Shapes the 'run' table in the database
    run_id: primary key
    tournament_id: foreign key
    run_time
    seed

    Related tables:
        * submission_run_info
        * tournament
        * turn
    """

    __tablename__: str = 'run'
    run_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    tournament_id: Mapped[int] = mapped_column(Integer(), ForeignKey("tournament.tournament_id", ondelete='CASCADE'))
    run_time: Mapped[str] = mapped_column(TimeStamp(), nullable=False)
    seed: Mapped[int] = mapped_column(Integer(), nullable=False)

    # results is a JSON file that's read in, so it needs to be a LargeBinary object.
    results: Mapped[str] = mapped_column(LargeBinary(), nullable=False)

    submission_run_infos: Mapped[list['SubmissionRunInfo']] = relationship(back_populates='run')
    tournament: Mapped['Tournament'] = relationship(back_populates='runs')
    turns: Mapped[list['Turn']] = relationship(back_populates='run')
