from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import BookingResponse


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingResponse
