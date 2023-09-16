from sqlalchemy import Integer, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class University(Base):
    __tablename__: str = 'university'
    uni_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    uni_name: Mapped[str] = mapped_column(String(100), CheckConstraint("uni_name != ''"), nullable=False, unique=True)
