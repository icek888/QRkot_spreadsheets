from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityRoom(CRUDBase):
    """Класс для реализации уникальных методов модели проектов."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        """Получить по названию благотворительного проекта его id."""
        result = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return result.scalars().first()


charity_project_crud = CRUDCharityRoom(CharityProject)
