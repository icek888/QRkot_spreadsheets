from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint
from sqlalchemy.sql import false

from app.core.db import Base


class InvestmentBase(Base):
    """Абстрактная базовая модель для моделей Пожертвования и Благ проекта."""
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=false(), nullable=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint("full_amount > 0", name="check_full_amount_positive"),
        CheckConstraint("0 <= invested_amount <= full_amount",
                        name="check_invested_amount_valid")
    )

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}('
            f'{self.full_amount=}, '
            f'{self.invested_amount=}, '
            f'{self.fully_invested=}, '
            f'{self.create_date=}, '
            f'{self.close_date=}'
            ')'
        )
