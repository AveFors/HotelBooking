from typing import Annotated
from datetime import date

from fastapi import APIRouter, HTTPException, Query

from src.models.facilities import RoomsFacilitiesOrm
from src.schemas.facilities import RoomFacilityCreate
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
    pagination: PaginationDep,
    date_to: date,
    date_from: date,
):
    return await db.rooms.get_filtered_by_time(
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1),
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
    new_room = RoomAdd(hotel_id=hotel_id, **room.model_dump())
    created_room = await db.rooms.add(schema=new_room)

    rooms_facilities = [
        RoomFacilityCreate(room_id=created_room.id, facility_id=f_id)
        for f_id in (room.facility_ids or [])
    ]

    await db.room_facilities.add_bulk(rooms_facilities)
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
        exclude={"facility_ids"},
    )

    result = await db.room_facilities.set_rooms_facilities(
        room_id=room_id,
        facility_ids=room.facility_ids,
    )

    await db.commit()
    update_room.facility_ids = sorted(result["new_ids"])
    return {"status": "OK", "data": update_room}


@router.patch("/{room_id}", summary="Частично обновить комнату")
async def update_hotel_room_patch(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room: RoomUpdatePatch,
):
    values = room.model_dump(
        exclude_unset=True,
        exclude={"facility_ids"},
    )
    if values:
        update_room = await db.rooms.edit(
            room,
            hotel_id=hotel_id,
            id=room_id,
            exclude_unset=True,
            exclude={"facility_ids"},
        )
    else:
        update_room = await db.rooms.get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )
        if update_room is None:
            raise HTTPException(
                status_code=404,
                detail="Комната не найдена",
            )

    if room.facility_ids is not None:
        result = await db.room_facilities.set_rooms_facilities(
            room_id=room_id,
            facility_ids=room.facility_ids,
        )
        response_ids = result["new_ids"]
    else:
        links = await db.room_facilities.get_all(room_id=room_id)
        response_ids = {link.facility_id for link in links}

    await db.commit()
    update_room.facility_ids = sorted(response_ids)
    return {"status": "OK", "data": update_room}


@router.delete("/{room_id}", summary="Удалить комнату")
async def delete_hotel_room(db: DBDep, hotel_id: int, room_id: int):
    delete_room = await db.rooms.delete(
        hotel_id=hotel_id,
        id=room_id,
    )
    await db.commit()
    return {"status": "OK", "data": delete_room}
