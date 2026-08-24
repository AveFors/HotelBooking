from sqlalchemy import select

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelResponse


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = HotelResponse

    async def get_all(self, substring, limit, offset):
        query = select(self.model)

        if substring:
            query = (
                query.filter(
                    (self.model.title.ilike(f"%{substring}%"))
                    | (self.model.location.ilike(f"%{substring}%"))
                )
                .order_by(self.model.id)
                .limit(limit)
                .offset(offset)
            )
        else:
            query = query.order_by(self.model.id).limit(limit).offset(offset)

        result = await self.session.execute(query)
        return [
            self.schema.model_validate(orm, from_attributes=True)
            for orm in result.scalars().all()
        ]
