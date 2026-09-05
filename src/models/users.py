from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        index=True,
    )
    hashed_password: Mapped[str] = mapped_column(String(200))
