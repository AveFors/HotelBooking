from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.facilities import FacilityCreate

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
async def get_facilities(db: DBDep, pagination: PaginationDep):
    return await db.facilities.get_all_by_pagination(
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1),
    )


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
