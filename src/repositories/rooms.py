from datetime import date

from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomResponse


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomResponse

    # async def get_all(
    #     self,
    #     substring: str,
    #     limit: int,
    #     offset: int,
    #     hotel_id: int,
    # ):
    #     query = select(self.model).filter_by(hotel_id=hotel_id)

    #     if substring:
    #         stmt = (
    #             query.filter(
    #                 self.model.description.ilike(f"%{substring}%")
    #                 | self.model.title.ilike(f"%{substring}%")
    #             )
    #             .order_by(self.model.id)
    #             .limit(limit)
    #             .offset(offset)
    #         )
    #     else:
    #         stmt = query.order_by(self.model.id).limit(limit).offset(offset)

    #     result = await self.session.execute(stmt)
    #     return [
    #         self.schema.model_validate(orm, from_attributes=True)
    #         for orm in result.scalars().all()
    #     ]

    async def get_filtered_by_time(
        self,
        limit: int,
        offset: int,
        hotel_id: int,
        date_to: date,
        date_from: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id,
            date_to=date_to,
            date_from=date_from,
        )

        return await self.get_all_by_pagination(
            limit,
            offset,
            RoomsOrm.id.in_(rooms_ids_to_get),
        )
