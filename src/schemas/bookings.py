from datetime import date, datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingCreate(BookingBase):
    pass


class BookingAdd(BookingBase):
    user_id: int
    price: int


class BookingResponse(BookingAdd):
    id: int
    total_cost: int
    created_at: datetime
