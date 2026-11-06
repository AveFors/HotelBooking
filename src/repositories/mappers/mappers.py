from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import BookingResponse
from src.schemas.facilities import FacilityResponse, RoomFacilityResponse
from src.schemas.hotels import HotelResponse
from src.schemas.rooms import RoomResponse, RoomWithRels
from src.schemas.users import UserResponse, UserResponseWithHashPass


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = HotelResponse


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomResponse


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserResponse


class UserWithHashPassDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserResponseWithHashPass


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = BookingResponse


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = FacilityResponse


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomFacilityResponse
