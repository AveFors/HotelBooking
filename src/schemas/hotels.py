from pydantic import BaseModel, ConfigDict


class HotelCreate(BaseModel):
    title: str
    location: str


class HotelResponse(HotelCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
