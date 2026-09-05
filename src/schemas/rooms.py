from pydantic import BaseModel


class RoomBase(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomCreate(RoomBase):
    pass


class RoomAdd(RoomCreate):
    hotel_id: int


class RoomUpdatePUT(RoomBase):
    description: str


class RoomUpdatePatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomResponse(RoomBase):
    id: int
    hotel_id: int
