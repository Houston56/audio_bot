import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import BOT_TOKEN
from core.database import engine, Base
from bot.handlers.user_audio import router as audio_router

async def main():
    # если это первый запуск без Alembic-upgrade — создаст таблицы и не упадёт
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(audio_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
