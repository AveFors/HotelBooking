from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import MultipleResultsFound, NoResultFound


class BaseRepository:
    model = None
    schema = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(orm, from_attributes=True)
            for orm in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        return self.schema.model_validate(orm, from_attributes=True)

    async def add(self, schema: BaseModel):
        stmt = insert(self.model).values(**schema.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return self.schema.model_validate(result.scalar_one(), from_attributes=True)

    async def edit(
        self,
        schema: BaseModel,
        exclude_unset=False,
        exclude_none=False,
        **filter_by,
    ):
        values = schema.model_dump(
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
        )
        if not values:
            raise HTTPException(
                status_code=400, detail="Не переданы поля для обновления."
            )
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**values)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        try:
            model = result.scalar_one()
        except MultipleResultsFound as exc:
            await self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Объектов для редактирования не может быть больше одного.",
            ) from exc
        except NoResultFound as exc:
            await self.session.rollback()
            raise HTTPException(
                status_code=404,
                detail="Объектов для редактирования не нашлось.",
            ) from exc
        else:
            return self.schema.model_validate(model, from_attributes=True)

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            hotel = result.scalar_one()
        except MultipleResultsFound as exc:
            await self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Объектов для удаления не может быть больше одного.",
            ) from exc
        except NoResultFound as exc:
            await self.session.rollback()
            raise HTTPException(
                status_code=404, detail="Объектов для удаления не нашлось."
            ) from exc
        else:
            return self.schema.model_validate(hotel, from_attributes=True)
