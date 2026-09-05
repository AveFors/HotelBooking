from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomCreate, RoomUpdatePatch, RoomUpdatePUT

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Комнаты"])


@router.get("/{room_id}", summary="Получить комнату по ID")
async def get_hotel_room_by_id(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(
            hotel_id=hotel_id,
            id=room_id,
        )

        if room is None:
            raise HTTPException(
                status_code=404,
                detail="Комната не найдена.",
            )

        return room


@router.get("/", summary="Получить все комнаты отеля")
async def get_hotel_rooms(
    pagination: PaginationDep,
    hotel_id: int,
    substring: Annotated[str | None, Query(min_length=2)] = None,
):
    limit = pagination.per_page
    offset = pagination.per_page * (pagination.page - 1)
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(
            substring=substring,
            limit=limit,
            offset=offset,
            hotel_id=hotel_id,
        )
        return rooms


@router.post("/", summary="Создать комнату в отеле")
async def create_hotel_room(
    hotel_id: int,
    room: RoomCreate,
):
    async with async_session_maker() as session:
        room = RoomAdd(hotel_id=hotel_id, **room.model_dump())
        created_room = await RoomsRepository(session).add(schema=room)
        await session.commit()
        return {"status": "OK", "data": created_room}


@router.put("/{room_id}", summary="Полностью обновить комнату")
async def update_hotel_room_put(
    hotel_id: int,
    room_id: int,
    room: RoomUpdatePUT,
):
    async with async_session_maker() as session:
        update_room = await RoomsRepository(session).edit(
            room,
            hotel_id=hotel_id,
            id=room_id,
        )
        await session.commit()
        return {"status": "OK", "data": update_room}


@router.patch("/{room_id}", summary="Частично обновить комнату")
async def update_hotel_room_patch(
    hotel_id: int,
    room_id: int,
    room: RoomUpdatePatch,
):
    async with async_session_maker() as session:
        update_room = await RoomsRepository(session).edit(
            room,
            hotel_id=hotel_id,
            id=room_id,
            exclude_unset=True,
        )
        await session.commit()
        return {"status": "OK", "data": update_room}


@router.delete("/{room_id}", summary="Удалить комнату")
async def delete_hotel_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        delete_room = await RoomsRepository(session).delete(
            hotel_id=hotel_id,
            id=room_id,
        )
        await session.commit()
        return {"status": "OK", "data": delete_room}
