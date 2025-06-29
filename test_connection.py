import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from core.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)


async def test_connection():
    print("🚀 Запуск test_connection()")
    try:
        async with engine.connect() as conn:
            print("🔗 Установлено соединение с базой")
            result = await conn.execute(text("SELECT 1"))
            print(result.fetchall())
            print("✅ Подключение к базе успешно")
    except Exception as e:
        print("❌ Ошибка подключения:", e)


if __name__ == "__main__":
    asyncio.run(test_connection())
