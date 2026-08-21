from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Query,
)
from sqlalchemy import Result, insert, select

from src.api.dependencies import Pagination
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelCreate, HotelResponse

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Получить все отели")
async def get_hotels(
    pagination: Annotated[Pagination, Query()],
    substring: Annotated[str | None, Query(min_length=2)] = None,
) -> list[HotelResponse]:

    _limit = pagination.per_page
    _offset = pagination.per_page * (pagination.page - 1)

    query = select(HotelsOrm)

    if substring:
        query = (
            query.filter(
                (HotelsOrm.title.ilike(f"%{substring}%"))
                | (HotelsOrm.location.ilike(f"%{substring}%"))
            )
            .order_by(HotelsOrm.id)
            .limit(_limit)
            .offset(_offset)
        )
    else:
        query = query.order_by(HotelsOrm.id).limit(_limit).offset(_offset)

    async with async_session_maker() as session:
        result: Result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.get("/{hotel_id}", summary="Получить отель по айди")
async def get_hotel_by_id(
    hotel_id: int,
) -> HotelResponse:
    async with async_session_maker() as session:
        return await session.get(HotelsOrm, hotel_id)


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
):
    async with async_session_maker() as session:
        stmt = insert(HotelsOrm).values(**hotel.model_dump())
        await session.execute(stmt)
        await session.commit()
    return {"status": "OK"}
