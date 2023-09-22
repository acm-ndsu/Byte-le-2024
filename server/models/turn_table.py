from sqlalchemy import LargeBinary, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TurnTable(Base):
    __tablename__: str = 'turn_table'
    turn_id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    turn_number: Mapped[int] = mapped_column(Integer())
    run_id: Mapped[int] = mapped_column(Integer(), ForeignKey('run.run_id'))
    turn_data: Mapped[str] = mapped_column(LargeBinary(), nullable=False)


