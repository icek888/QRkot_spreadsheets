from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.schemas.base import BaseDB


class CharityProjectBase(BaseModel):
    """Базовая pydantic-схема благотворительного проекта."""
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectUpdate(BaseModel):
    """Pydantic-схема для обновления благотворительного проекта.
    Все поля опциональны, что позволяет выполнять частичные обновления.
    """
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1
        schema_extra = {
            'example': {
                'name': 'Toys for cats',
                'description': 'Cats need to have fun',
                'full_amount': 10000
            }
        }

    @validator('name', 'description', 'full_amount', pre=True, always=True)
    def fields_cannot_be_null(cls, value, field):
        """
        Проверяет, что если поле присутствует, его значение не равно None.
        Если поле отсутствует, оно не обрабатывается валидатором.
        """
        if value is None:
            return value
        if isinstance(value, str) and not value.strip():
            raise ValueError(f'Поле "{field.name}" не может быть пустым!')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    """Pydantic-схема для создания благотворительного проекта."""
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectBase, BaseDB):
    """Pydantic-схема для вывода информации о благотворительном проекте."""
