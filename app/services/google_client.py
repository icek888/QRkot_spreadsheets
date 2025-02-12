from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import copy

from aiogoogle import Aiogoogle
from app.core.config import settings

DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'
DEFAULT_ROW_COUNT = settings.sheet_row_count
DEFAULT_COLUMN_COUNT = settings.sheet_column_count

TABLE_HEADER_TEMPLATE: List[List[str]] = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]

SPREADSHEET_BODY_TEMPLATE: Dict = {
    'properties': {
        'title': '',
        'locale': 'ru_RU',
    },
    'sheets': [
        {
            'properties': {
                'sheetId': 0,
                'title': '',
                'sheetType': 'GRID',
                'gridProperties': {
                    'rowCount': DEFAULT_ROW_COUNT,
                    'columnCount': DEFAULT_COLUMN_COUNT,
                },
            },
        }
    ],
}

USER_PERMISSION_BODY: Dict = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email,
}


def get_table_header() -> List[List[str]]:
    """Возвращает шапку таблицы с подставленной датой."""
    header = copy.deepcopy(TABLE_HEADER_TEMPLATE)
    header[0][1] = datetime.now().strftime(DATETIME_FORMAT)
    return header


def build_spreadsheet_body() -> Dict:
    """Формирует тело гугл-таблицы с актуальной датой создания отчета."""
    title = (
        f'{settings.report_title} от '
        f'{datetime.now().strftime(DATETIME_FORMAT)}'
    )
    spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY_TEMPLATE)
    spreadsheet_body['properties']['title'] = title
    spreadsheet_body['sheets'][0]['properties']['title'] = title
    return spreadsheet_body


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle,
) -> None:
    """Выдача прав доступа личному гугл-аккаунту к документу."""
    service = await wrapper_service.discover(
        'drive',
        settings.google_drive_api_version
    )
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=USER_PERMISSION_BODY,
            fields='id',
        )
    )


async def spreadsheets_create(wrapper_service: Aiogoogle) -> Tuple[str, str]:
    """Создание гугл-таблицы. Возвращает идентификатор и URL отчёта."""
    service = await wrapper_service.discover(
        'sheets',
        settings.google_sheets_api_version
    )
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=build_spreadsheet_body())
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List,
    wrapper_service: Aiogoogle,
) -> None:
    """Формирование отчета в гугл-таблице на основе данных."""
    service = await wrapper_service.discover(
        'sheets',
        settings.google_sheets_api_version
    )
    data_rows = [
        [
            str(project[0]),
            str(timedelta(days=project[1])),
            str(project[2]),
        ]
        for project in projects
    ]
    table_values = get_table_header() + data_rows
    num_rows = len(table_values)
    num_cols = max(map(len, table_values))
    if num_rows > DEFAULT_ROW_COUNT or num_cols > DEFAULT_COLUMN_COUNT:
        raise ValueError(
            f'Данные отчёта превышают размеры листа: {num_rows} строк '
            f'(макс {DEFAULT_ROW_COUNT}) или {num_cols} столбцов '
            f'(макс {DEFAULT_COLUMN_COUNT}).'
        )
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{num_rows}C{num_cols}',
            valueInputOption='USER_ENTERED',
            json={'majorDimension': 'ROWS', 'values': table_values},
        )
    )


async def get_spreadsheets_from_disk(
    spreadsheet_title: str,
    wrapper_service: Aiogoogle,
) -> List[Dict[str, str]]:
    """Получить список всех сформированных отчетов."""
    service = await wrapper_service.discover(
        'drive',
        settings.google_drive_api_version
    )
    q = (
        f'mimeType="application/vnd.google-apps.spreadsheet" '
        f'and name="{spreadsheet_title}"'
    )
    spreadsheets = await wrapper_service.as_service_account(
        service.files.list(q=q)
    )
    return spreadsheets['files']


async def delete_spreadsheets_from_disk(wrapper_service: Aiogoogle) -> None:
    """Удалить все отчеты с диска."""
    service = await wrapper_service.discover(
        'drive',
        settings.google_drive_api_version
    )
    spreadsheets = await get_spreadsheets_from_disk(
        settings.report_title,
        wrapper_service
    )
    for spreadsheet in spreadsheets:
        await wrapper_service.as_service_account(
            service.files.delete(fileId=spreadsheet['id'])
        )
