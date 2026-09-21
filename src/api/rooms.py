from typing import Annotated
from datetime import date

from fastapi import APIRouter, HTTPException, Query

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.rooms import RoomAdd, RoomCreate, RoomUpdatePatch, RoomUpdatePUT

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Комнаты"])


@router.get("/{room_id}", summary="Получить комнату по ID")
async def get_hotel_room_by_id(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    room = await db.rooms.get_one_or_none(
        hotel_id=hotel_id,
        id=room_id,
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Комната не найдена.",
        )

    return room


# @router.get("/", summary="Получить все комнаты отеля")
# async def get_hotel_rooms(
#     db: DBDep,
#     pagination: PaginationDep,
#     hotel_id: int,
#     substring: Annotated[str | None, Query(min_length=2)] = None,
# ):
#     limit = pagination.per_page
#     offset = pagination.per_page * (pagination.page - 1)
#     rooms = await db.rooms.get_all(
#         substring=substring,
#         limit=limit,
#         offset=offset,
#         hotel_id=hotel_id,
#     )
#     return rooms


@router.get("/")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_to: date,
    date_from: date,
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_to=date_to,
        date_from=date_from,
    )


@router.post("/", summary="Создать комнату в отеле")
async def create_hotel_room(
    db: DBDep,
    hotel_id: int,
    room: RoomCreate,
):
    room = RoomAdd(hotel_id=hotel_id, **room.model_dump())
    created_room = await db.rooms.add(schema=room)
    await db.commit()
    return {"status": "OK", "data": created_room}


@router.put("/{room_id}", summary="Полностью обновить комнату")
async def update_hotel_room_put(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room: RoomUpdatePUT,
):
    update_room = await db.rooms.edit(
        room,
        hotel_id=hotel_id,
        id=room_id,
    )
    await db.commit()
    return {"status": "OK", "data": update_room}


@router.patch("/{room_id}", summary="Частично обновить комнату")
async def update_hotel_room_patch(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room: RoomUpdatePatch,
):
    update_room = await db.rooms.edit(
        room,
        hotel_id=hotel_id,
        id=room_id,
        exclude_unset=True,
    )
    await db.commit()
    return {"status": "OK", "data": update_room}


@router.delete("/{room_id}", summary="Удалить комнату")
async def delete_hotel_room(db: DBDep, hotel_id: int, room_id: int):
    delete_room = await db.rooms.delete(
        hotel_id=hotel_id,
        id=room_id,
    )
    await db.commit()
    return {"status": "OK", "data": delete_room}
