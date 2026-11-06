from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    # async def get_all(self, substring, limit, offset):
    #     query = select(self.model)

    #     if substring:
    #         stmt = (
    #             query.filter(
    #                 (self.model.title.ilike(f"%{substring}%"))
    #                 | (self.model.location.ilike(f"%{substring}%"))
    #             )
    #             .order_by(self.model.id)
    #             .limit(limit)
    #             .offset(offset)
    #         )
    #     else:
    #         stmt = query.order_by(self.model.id).limit(limit).offset(offset)

    #     result = await self.session.execute(stmt)
    #     return [
    #         self.mapper.map_to_domain_entity(orm)
    #         for orm in result.scalars().all()
    #     ]

    async def get_filtered_by_time(
        self,
        limit: int,
        offset: int,
        date_from: date,
        date_to: date,
        substring: str | None = None,
    ):

        rooms_ids_for_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
        )

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_for_get))
        )

        filters = [
            HotelsOrm.id.in_(hotels_ids_to_get),
        ]

        if substring:
            filters.append(
                self.model.title.ilike(f"%{substring}%")
                | self.model.location.ilike(f"%{substring}%")
            )

        return await self.get_all_by_pagination(
            limit,
            offset,
            *filters,
        )
