from sqlalchemy import LargeBinary, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Submission(Base):
    __tablename__: str = 'submission'
    submission_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    team_id_uuid: Mapped[int] = mapped_column(Integer(), ForeignKey("team.team_id_uuid"))
    submission_time: Mapped[str] = mapped_column(DateTime(), nullable=False)
    file_txt: Mapped[str] = mapped_column(LargeBinary(), nullable=False)
