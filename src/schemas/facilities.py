from pydantic import BaseModel


class FacilityBase(BaseModel):
    title: str


class FacilityCreate(FacilityBase):
    pass


class FacilityResponse(FacilityBase):
    id: int


class RoomFacilityBase(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilityCreate(RoomFacilityBase):
    pass


class RoomFacilityResponse(RoomFacilityBase):
    id: int
