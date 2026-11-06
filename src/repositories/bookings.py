from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_today(self):
        query = select(BookingsOrm).filter_by(date_from=date.today())
        result = await self.session.execute(query)
        print(result)
        return [
            self.mapper.map_to_domain_entity(booking)
            for booking in result.scalars().all()
        ]
