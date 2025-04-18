from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = 'QRKot Charity Fund'
    DATABASE_URL: str = 'sqlite+aiosqlite:///./qrkot_charity_fund.db'
    SECRET: str = 'supersecretkey'
    FIRST_SUPERUSER_EMAIL: str = 'admin@example.com'
    FIRST_SUPERUSER_PASSWORD: str = 'changeme'
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    report_title: str = 'Charity projects report'
    google_drive_api_version: str = 'v3'
    google_sheets_api_version: str = 'v4'
    sheet_row_count: int = 100
    sheet_column_count: int = 10

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
