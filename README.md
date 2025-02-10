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

---

## Технологии

- **Python 3.9+**
- **FastAPI** (REST API)
- **SQLAlchemy + Alembic** (База данных)
- **Pydantic** (Валидация данных)
- **FastAPI Users** (Аутентификация)
- **SQLite** (База данных по умолчанию)
- **Pytest** (Тестирование)

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

---

## Автор

**Karlen Abelyan**

[Icek888](https://github.com/Icek888) – разработчик проекта QRKot

---
