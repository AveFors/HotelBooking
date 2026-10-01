from sqlalchemy import select

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import (
    FacilityResponse,
    RoomFacilityCreate,
    RoomFacilityResponse,
)


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = FacilityResponse


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacilityResponse

    async def set_rooms_facilities(
        self,
        room_id,
        facility_ids: list[int],
    ):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)
        old_ids = set(result.scalars().all())
        new_ids = set(facility_ids)

        to_delete = old_ids - new_ids
        to_add = new_ids - old_ids

        if to_delete:
            await self.delete_bulk(
                RoomsFacilitiesOrm.facility_id.in_(to_delete),
                room_id=room_id,
            )

        if to_add:
            rooms_facilities_to_add = [
                RoomFacilityCreate(room_id=room_id, facility_id=f_id) for f_id in to_add
            ]
            await self.add_bulk(rooms_facilities_to_add)

        return {"old_ids": old_ids, "new_ids": new_ids}
