from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services.google_client import (
    get_spreadsheets_from_disk,
    delete_spreadsheets_from_disk,
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post('/', dependencies=[Depends(current_superuser)])
async def get_project_progress_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
    current_user=Depends(current_superuser),
) -> dict[str, str]:
    """
    Создание гугл-таблицы с отчетом по закрытым благотворительным проектам,
    отсортированных по скорости сбора средств. Только для суперюзеров.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id, spreadsheet_url = await spreadsheets_create(
        wrapper_service
    )
    await set_user_permissions(
        spreadsheet_id,
        wrapper_service
    )
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            projects,
            wrapper_service
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Данные отчёта не подходят под ограничения листа: {exc}"
        ) from exc
    return {'google_sheet_url': spreadsheet_url}


@router.get('/', dependencies=[Depends(current_superuser)])
async def get_all_reports(
    wrapper_service: Aiogoogle = Depends(get_service),
) -> list[dict[str, str]]:
    """
    Получить список ранее сформированных отчетов.
    """
    return await get_spreadsheets_from_disk(
        settings.report_title,
        wrapper_service
    )


@router.delete('/', dependencies=[Depends(current_superuser)])
async def clear_all_reports(
    wrapper_service: Aiogoogle = Depends(get_service),
) -> dict[str, str]:
    """
    Очистить диск от сформированных отчетов.
    """
    await delete_spreadsheets_from_disk(wrapper_service)
    return {'message': 'All reports were deleted.'}
