from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    '''Базовый класс для выполнения операций CRUD.'''

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        '''Получить объект модели по id.'''
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> List[ModelType]:
        '''Получить список объектов модели.'''
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(
        self,
        data: CreateSchemaType,
        session: AsyncSession,
        user: Optional[User] = None,
        commit: bool = True,
    ) -> ModelType:
        '''Создать объект модели и записать в БД.'''
        new_obj_data = data.dict()
        if user is not None:
            new_obj_data['user_id'] = user.id
        new_obj = self.model(**new_obj_data)
        session.add(new_obj)
        if commit:
            await session.commit()
            await session.refresh(new_obj)
        return new_obj

    async def get_active_objs(
        self,
        session: AsyncSession,
    ) -> List[ModelType]:
        '''Получить список активных объектов модели.'''
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested == false())
            .order_by(self.model.id)
        )
        return result.scalars().all()

    async def update(
        self,
        db_obj: ModelType,
        data: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        '''Обновить объект модели.'''
        if hasattr(data, 'dict'):
            update_data = data.dict(exclude_unset=True)
        else:
            update_data = data

        for field, value in update_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db_obj: ModelType,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        '''Удалить объект модели.'''
        await session.delete(db_obj)
        if commit:
            await session.commit()
        return db_obj
