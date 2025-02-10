from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """Класс для реализации уникальных методов модели пожертвований."""

    async def get_user_donation(
        self,
        session: AsyncSession,
        user: User
    ) -> list[Donation]:
        """Получить список пожертвований текущего пользователя."""
        result = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
