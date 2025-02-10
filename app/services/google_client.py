from datetime import datetime, timedelta
from typing import List, Dict, Tuple

from aiogoogle import Aiogoogle
from app.core.config import settings

DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

DEFAULT_ROW_COUNT = getattr(settings, 'sheet_row_count', 100)
DEFAULT_COLUMN_COUNT = getattr(settings, 'sheet_column_count', 10)

TABLE_HEADER_TEMPLATE: List[List[str]] = [
    ['Отчет от', '{report_date}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]


def get_table_header() -> List[List[str]]:
    '''Возвращает шапку таблицы с подставленной датой.'''
    current_date = datetime.now().strftime(DATETIME_FORMAT)
    return [
        [
            cell.format(report_date=current_date)
            if '{report_date}' in cell else cell
            for cell in row
        ]
        for row in TABLE_HEADER_TEMPLATE
    ]


def build_sheet_body() -> Dict:
    '''Формирует тело листа с динамическими размерами.'''
    title_str = (
        f'{settings.report_title} от '
        f'{datetime.now().strftime(DATETIME_FORMAT)}'
    )
    return {
        'properties': {
            'sheetId': 0,
            'title': title_str,
            'sheetType': 'GRID',
            'gridProperties': {
                'rowCount': DEFAULT_ROW_COUNT,
                'columnCount': DEFAULT_COLUMN_COUNT,
            },
        },
    }


SPREADSHEET_BODY: Dict = {
    'properties': {
        'title': (
            f'{settings.report_title} от '
            f'{datetime.now().strftime(DATETIME_FORMAT)}'
        ),
        'locale': 'ru_RU',
    },
    'sheets': [build_sheet_body()],
}

USER_PERMISSION_BODY: Dict = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email,
}


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle,
) -> None:
    '''Выдача прав доступа личному гугл-аккаунту к документу.'''
    service = await wrapper_service.discover(
        'drive',
        settings.google_drive_api_version,
    )
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=USER_PERMISSION_BODY,
            fields='id',
        )
    )


async def spreadsheets_create(
    wrapper_service: Aiogoogle,
) -> Tuple[str, str]:
    '''Создание гугл-таблицы. Возвращает идентификатор и URL отчёта.'''
    service = await wrapper_service.discover(
        'sheets',
        settings.google_sheets_api_version,
    )
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    spreadsheet_url = response.get('spreadsheetUrl', '')
    return spreadsheet_id, spreadsheet_url


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List,
    wrapper_service: Aiogoogle,
) -> None:
    '''Формирование отчета в гугл-таблице на основе данных.'''
    service = await wrapper_service.discover(
        'sheets',
        settings.google_sheets_api_version,
    )

    header = get_table_header()

    data_rows = [
        [
            str(project[0]),
            str(timedelta(days=project[1])),
            str(project[2]),
        ]
        for project in projects
    ]

    table_values = header + data_rows

    num_rows = len(table_values)
    num_cols = len(table_values[0]) if table_values else 0
    if num_rows > DEFAULT_ROW_COUNT or num_cols > DEFAULT_COLUMN_COUNT:
        raise ValueError('Данные отчёта превышают размеры листа.')

    update_range = f'R1C1:R{num_rows}C{num_cols}'

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=update_range,
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )


async def get_spreadsheets_from_disk(
    spreadsheet_title: str,
    wrapper_service: Aiogoogle,
) -> List[Dict[str, str]]:
    '''Получить список всех сформированных отчетов.'''
    service = await wrapper_service.discover(
        'drive',
        settings.google_drive_api_version,
    )
    q = (
        f'mimeType="application/vnd.google-apps.spreadsheet" '
        f'and name="{spreadsheet_title}"'
    )
    spreadsheets = await wrapper_service.as_service_account(
        service.files.list(q=q)
    )
    return spreadsheets['files']


async def delete_spreadsheets_from_disk(
    wrapper_service: Aiogoogle,
) -> None:
    '''Удалить все отчеты с диска.'''
    service = await wrapper_service.discover(
        'drive',
        settings.google_drive_api_version,
    )
    spreadsheets = await get_spreadsheets_from_disk(
        settings.report_title, wrapper_service
    )
    for spreadsheet in spreadsheets:
        await wrapper_service.as_service_account(
            service.files.delete(fileId=spreadsheet['id'])
        )
