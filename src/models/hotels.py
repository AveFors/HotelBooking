from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
