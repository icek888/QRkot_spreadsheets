
---

# QRKot Charity Fund

QRKot — это платформа для сбора пожертвований на благотворительные проекты. Пользователи могут делать пожертвования, а администраторы управлять проектами.

---

## Функционал

- **Создание благотворительных проектов**
- **Внесение пожертвований**
- **Автоматическое распределение средств**
- **Авторизация пользователей**
  - Роли: пользователь / суперпользователь
- **Просмотр собранных сумм**
- **Создание отчетов в Google Sheets**  
  Автоматическая генерация таблиц с отчетами по закрытым проектам, обновление данных и управление доступом через Google API.

---

## Технологии

- **Python 3.9+**
- **FastAPI** (REST API)
- **SQLAlchemy + Alembic** (База данных)
- **Pydantic** (Валидация данных)
- **FastAPI Users** (Аутентификация)
- **SQLite** (База данных по умолчанию)
- **Pytest** (Тестирование)
- **Google API**  
  Использование Google Sheets API (v4) и Google Drive API (v3) для создания и управления отчетными таблицами.

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-repository/qrcot-charity-fund.git
cd qrcot-charity-fund
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate     # Для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск миграций Alembic

```bash
alembic upgrade head
```

### 5. Запуск сервера

```bash
uvicorn app.main:app --reload
```

Сервер запустится по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Документация API:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Запуск тестов

```bash
pytest
```

---

## Переменные окружения

Создайте файл `.env` и укажите следующие переменные:

```ini
DATABASE_URL=sqlite+aiosqlite:///./example.db
SECRET=your-secret-key
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=changeme

# Переменные для Google API (необходимы для работы с Google Sheets и Drive)
TYPE=your-google-type
PROJECT_ID=your-google-project-id
PRIVATE_KEY_ID=your-google-private-key-id
PRIVATE_KEY=your-google-private-key
CLIENT_EMAIL=your-google-client-email
CLIENT_ID=your-google-client-id
AUTH_URI=your-google-auth-uri
TOKEN_URI=your-google-token-uri
AUTH_PROVIDER_X509_CERT_URL=your-google-auth-provider-x509-cert-url
CLIENT_X509_CERT_URL=your-google-client-x509-cert-url
```

---

## Использование API

### Регистрация и вход

- **Регистрация**: `POST /auth/register`
- **Авторизация**: `POST /auth/jwt/login`

### Работа с проектами

- **Создать проект**: `POST /charity_project/`
- **Получить список проектов**: `GET /charity_project/`
- **Обновить проект**: `PATCH /charity_project/{id}`
- **Удалить проект**: `DELETE /charity_project/{id}`

### Работа с пожертвованиями

- **Сделать пожертвование**: `POST /donation/`
- **Получить мои пожертвования**: `GET /donation/my`
- **Получить все пожертвования (для суперпользователя)**: `GET /donation/`

### Работа с отчетами (Google Sheets API)

_Эти эндпоинты доступны только для суперпользователей._

- **Создать отчет**: `POST /report/`  
  Создает таблицу в Google Sheets с отчетом по закрытым благотворительным проектам.  
  В ответе возвращается полный URL созданной таблицы, полученный от Google API.
- **Получить список отчетов**: `GET /report/`  
  Получить список ранее сформированных отчетов.
- **Удалить все отчеты**: `DELETE /report/`  
  Удаляет все отчеты с диска (Google Drive).


---

### Объяснение логики работы с Google API

При создании отчета используется функция `spreadsheets_create`, которая отправляет запрос к Google Sheets API. В ответе API возвращаются как идентификатор таблицы, так и её полный URL (ключ `'spreadsheetUrl'`). Этот URL передается в ответе эндпоинта, что исключает необходимость формирования ссылки вручную.  
Также применяется функция `set_user_permissions` для выдачи прав доступа к таблице, а функция `spreadsheets_update_value` отвечает за заполнение таблицы данными. Все операции выполняются через официальный клиент Google API (Aiogoogle), что гарантирует корректность и актуальность ссылок и данных.

---

## Автор

**Karlen Abelyan**

[Icek888](https://github.com/Icek888) – разработчик проекта QRKot

---
