from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Errors(Base):
    __tablename__: str = 'errors'
    error_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)  # run id pk
    run_id: Mapped[int] = mapped_column(Integer(), ForeignKey("run.run_id"))  # run id
    submission_id: Mapped[int] = mapped_column(Integer(), ForeignKey("submission.submission_id"))  # submission id fk
    error_txt: Mapped[str] = mapped_column(String(), nullable=True)
