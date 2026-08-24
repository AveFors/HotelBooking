from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Query,
)

from repositories.hotels import HotelsRepository
from src.api.dependencies import Pagination
from src.database import async_session_maker
from src.schemas.hotels import (
    HotelCreate,
    HotelResponse,
    HotelUpdatePUT,
    HotelUpdatePatch,
)

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Получить все отели")
async def get_hotels(
    pagination: Annotated[Pagination, Query()],
    substring: Annotated[str | None, Query(min_length=2)] = None,
) -> list[HotelResponse]:
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            substring=substring,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )


@router.get("/{hotel_id}", summary="Получить отель по айди")
async def get_hotel_by_id(
    hotel_id: int,
) -> HotelResponse:
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)

        if hotel is None:
            raise HTTPException(
                status_code=404,
                detail="Такого отеля не существует.",
            )

        return hotel


@router.post(
    "/",
    summary="Создание отеля",
    description="<h1> Создаем отель с переданными данными. </h1>",
)
async def create_hotel(
    hotel: Annotated[
        HotelCreate,
        Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Отель в Сочи",
                        "location": "г. Сочи улица Пушкина",
                    },
                },
                "2": {
                    "summary": "Москва",
                    "value": {
                        "title": "Отель в Москве",
                        "location": "г. Москва улица Колотушкина",
                    },
                },
            }
        ),
    ],
) -> dict:
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(schema=hotel)
        await session.commit()
        return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменение отеля(PUT).")
async def update_put_hotel(hotel_id: int, hotel: HotelUpdatePUT) -> dict:
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(
            schema=hotel,
            id=hotel_id,
        )
        await session.commit()
        return {"status": "OK", "data": hotel}


@router.patch("/{hotel_id}", summary="Изменения отеля(PATCH)")
async def update_patch_hotel(hotel_id: int, hotel: HotelUpdatePatch) -> dict:
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(
            schema=hotel,
            id=hotel_id,
            exclude_none=True,
            exclude_unset=True,
        )
        await session.commit()
        return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля.")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "OK", "data": hotel}
