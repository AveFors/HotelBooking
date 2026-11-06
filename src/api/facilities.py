from typing import Annotated
import json

from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.facilities import FacilityCreate

from init_redis import redis

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
async def get_facilities(db: DBDep, pagination: PaginationDep):
    cache_key = f"facilities:page:{pagination.page}:per_page:{pagination.per_page}"
    facilities_in_cache = await redis.get(
        cache_key,
    )
    if facilities_in_cache is None:
        facilities = await db.facilities.get_all_by_pagination(
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )
        dict_facilities = [facility.model_dump() for facility in facilities]
        facilities_for_cache = json.dumps(dict_facilities)
        await redis.set(
            cache_key,
            facilities_for_cache,
            expire=10,
        )
        return facilities
    else:
        returning_cached_facilities = json.loads(facilities_in_cache)

        return returning_cached_facilities


@router.get("/{facility_id}")
async def get_facility_by_id(
    facility_id: int,
    db: DBDep,
):
    facility = await db.facilities.get_one_or_none(id=facility_id)

    if not facility:
        raise HTTPException(
            status_code=404,
            detail="Такого удобства не существует.",
        )
    return facility


@router.post("/")
async def create_facility(
    db: DBDep,
    schema: Annotated[FacilityCreate, Body()],
):
    facility = await db.facilities.add(schema)
    await db.commit()
    return {"status": "OK", "facility": facility}
