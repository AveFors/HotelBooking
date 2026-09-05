from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomResponse
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomResponse

    async def get_all(
        self,
        substring: str,
        limit: int,
        offset: int,
        hotel_id: int,
    ):
        query = select(self.model).filter_by(hotel_id=hotel_id)

        if substring:
            stmt = (
                query.filter(
                    self.model.description.ilike(f"%{substring}%")
                    | self.model.title.ilike(f"%{substring}%")
                )
                .order_by(self.model.id)
                .limit(limit)
                .offset(offset)
            )
        else:
            stmt = query.order_by(self.model.id).limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return [
            self.schema.model_validate(orm, from_attributes=True)
            for orm in result.scalars().all()
        ]
