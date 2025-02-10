from typing import List, Optional, Tuple

from sqlalchemy import func, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


class CRUDCharityRoom(CRUDBase[CharityProject, CharityProjectUpdate]):
    '''Класс для реализации уникальных методов модели CharityProject.'''

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        '''Получить по названию благотворительного проекта его id.'''
        return (
            await session.execute(
                select(self.model.id).where(self.model.name == project_name)
            )
        ).scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> List[Tuple[str]]:
        '''Получить список закрытых проектов с расчетом времени сбора.
        Время сбора указывается в днях.
        '''
        stmt = select(
            self.model.name,
            (func.julianday(self.model.close_date) -
             func.julianday(self.model.create_date)).label('rate'),
            self.model.description,
        ).where(self.model.fully_invested == true()).order_by('rate')
        return (await session.execute(stmt)).all()


charity_project_crud = CRUDCharityRoom(CharityProject)
