from datetime import date, datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("rooms.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    @hybrid_property
    def total_cost(self):
        return self.price * (self.date_to - self.date_from).days

    @total_cost.expression
    def total_cost(cls):
        return cls.price * (cls.date_to - cls.date_from)
