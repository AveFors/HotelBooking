from pydantic import BaseModel


class RoomBase(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facility_ids: list[int] | None = None


class RoomCreate(RoomBase):
    pass


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomUpdatePUT(RoomBase):
    description: str
    facility_ids: list[int]


class RoomUpdatePatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facility_ids: list[int] | None = None


class RoomResponse(RoomBase):
    id: int
    hotel_id: int
