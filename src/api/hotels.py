from datetime import date
from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Query,
)

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import (
    HotelCreate,
    HotelResponse,
    HotelUpdatePatch,
    HotelUpdatePUT,
)

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Получить все отели")
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date,
    date_to: date,
    substring: Annotated[str | None, Query(min_length=2)] = None,
) -> list[HotelResponse]:
    return await db.hotels.get_filtered_by_time(
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1),
        substring=substring,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}", summary="Получить отель по айди")
async def get_hotel_by_id(
    db: DBDep,
    hotel_id: int,
) -> HotelResponse:
    hotel = await db.hotels.get_one_or_none(id=hotel_id)

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
    db: DBDep,
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
    hotel = await db.hotels.add(schema=hotel)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменение отеля(PUT).")
async def update_put_hotel(db: DBDep, hotel_id: int, hotel: HotelUpdatePUT) -> dict:
    hotel = await db.hotels.edit(
        schema=hotel,
        id=hotel_id,
    )
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.patch("/{hotel_id}", summary="Изменения отеля(PATCH)")
async def update_patch_hotel(db: DBDep, hotel_id: int, hotel: HotelUpdatePatch) -> dict:
    hotel = await db.hotels.edit(
        schema=hotel,
        id=hotel_id,
        exclude_none=True,
        exclude_unset=True,
    )
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля.")
async def delete_hotel(db: DBDep, hotel_id: int):
    hotel = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK", "data": hotel}
