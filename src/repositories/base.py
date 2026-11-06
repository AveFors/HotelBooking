from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from src.database import Base
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: Base = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all_by_pagination(
        self,
        limit: int | None,
        offset: int | None,
        *filter,
        **filter_by,
    ):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(orm) for orm in result.scalars().all()]

    async def get_all(self, *filter, **filter_by):
        return await self.get_all_by_pagination(None, None, *filter, **filter_by)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        return self.mapper.map_to_domain_entity(orm)

    async def add(self, schema: BaseModel):
        stmt = insert(self.model).values(**schema.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return self.mapper.map_to_domain_entity(result.scalar_one())

    async def add_bulk(
        self,
        data: list[BaseModel],
    ):
        if data:
            stmt = insert(self.model).values([item.model_dump() for item in data])
            return await self.session.execute(stmt)
        return

    async def edit(
        self,
        schema: BaseModel,
        exclude_unset=False,
        exclude_none=False,
        exclude=None,
        **filter_by,
    ):
        values = schema.model_dump(
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude=exclude,
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
            return self.mapper.map_to_domain_entity(model)

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            model = result.scalar_one()
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
            return self.mapper.map_to_domain_entity(model)

    async def delete_bulk(self, *filters, **filter_by):
        stmt = delete(self.model).filter(*filters).filter_by(**filter_by)
        return await self.session.execute(stmt)
