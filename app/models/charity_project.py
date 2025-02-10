from sqlalchemy import Column, String, Text

from app.models.base import InvestmentBase


class CharityProject(InvestmentBase):
    """Модель Благотворительного проекта."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f"name={self.name}, description={self.description}, "
            f"{super().__repr__()}"
        )
