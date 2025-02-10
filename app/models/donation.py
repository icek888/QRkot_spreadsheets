from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    """Модель Пожертвования."""
    __tablename__ = 'donation'

    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)

    def __repr__(self) -> str:
        return (
            f'user_id={self.user_id}, comment={self.comment}, '
            f'{super().__repr__()}'
        )
