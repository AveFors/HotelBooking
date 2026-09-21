from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, PaginationDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("/", summary="Создание бронирования")
async def create_booking(
    user_id: UserIdDep,
    booking: BookingCreate,
    db: DBDep,
) -> dict:

    room = await db.rooms.get_one_or_none(id=booking.room_id)
    if not room:
        return HTTPException(status_code=404, detail="Комната не найдена.")

    add_booking = BookingAdd(
        **booking.model_dump(),
        room_id=booking.room_id,
        user_id=user_id,
        price=room.price,
    )
    added_booking = await db.bookings.add(add_booking)
    await db.commit()

    return {"status": "OK", "booking": added_booking}


@router.get("/", summary="Получение всех бронирований")
async def get_all_bookings(
    db: DBDep,
    pagination: PaginationDep,
) -> list[BookingResponse]:
    return await db.bookings.get_all_by_pagination(
        limit=pagination.per_page,
        offset=(pagination.per_page * (pagination.page - 1)),
    )


@router.get("/me", summary="Получение своих бронирований")
async def get_all_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
    pagination: PaginationDep,
) -> list[BookingResponse]:
    return await db.bookings.get_all_by_pagination(
        limit=pagination.per_page,
        offset=(pagination.per_page * (pagination.page - 1)),
        user_id=user_id,
    )
