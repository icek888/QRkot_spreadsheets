import asyncio
from sqlalchemy import text
from app.core.db import AsyncSessionLocal

async def update_superuser():
    async with AsyncSessionLocal() as session:
        # Выполняем запрос обновления через raw SQL
        await session.execute(
            text("UPDATE user SET is_superuser = 1 WHERE email = :email"),
            {"email": "admin@example.com"}
        )
        await session.commit()
        print("Пользователь admin@example.com обновлён, is_superuser установлен в 1.")

if __name__ == "__main__":
    asyncio.run(update_superuser())
