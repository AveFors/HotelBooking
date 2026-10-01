from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilityResponse, RoomFacilityResponse


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = FacilityResponse


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacilityResponse
