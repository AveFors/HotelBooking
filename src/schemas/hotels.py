from pydantic import BaseModel, ConfigDict


class HotelBase(BaseModel):
    title: str
    location: str


class HotelCreate(HotelBase):
    pass


class HotelUpdatePUT(HotelBase):
    pass


class HotelUpdatePatch(HotelBase):
    title: str | None = None
    location: str | None = None


class HotelResponse(HotelBase):
    id: int
