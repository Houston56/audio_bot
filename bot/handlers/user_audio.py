from pathlib import Path
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select

from core.database import get_session
from core.models import User, AudioFile
from core.config import MEDIA_FOLDER
from bot.utils.sanitize import sanitize

router = Router(name="user_audio")

# /start
@router.message(F.text == "/start")
async def cmd_start(msg: Message):
    await msg.answer("Привет! Пришли мне аудиофайл — я его сохраню. 🔊")

# любое аудио
@router.message(F.audio)
async def handle_audio(msg: Message):
    audio = msg.audio
    tg = msg.from_user

    async for session in get_session():
        # пользователь
        user = (await session.scalars(
            select(User).where(User.tg_id == tg.id)
        )).first()

        if not user:
            user = User(
                tg_id=tg.id,
                username=tg.username,
                first_name=tg.first_name,
                last_name=tg.last_name,
            )
            session.add(user)
            await session.commit()

        #проверяем, нет ли такого же файла у пользователя
        duplicate = await session.scalar(
            select(AudioFile.id).where(
               AudioFile.owner_id == user.id,
               AudioFile.file_unique_id == audio.file_unique_id,
            )
        )
        if duplicate:
            await msg.answer("🔁 Это аудио у тебя уже сохранено!")
            return

        # скачиваем файл
        user_dir = Path(MEDIA_FOLDER) / str(tg.id)
        user_dir.mkdir(parents=True, exist_ok=True)
        file = await msg.bot.get_file(audio.file_id)

        # красивое имя для фронта + безопасное имя на диске
        if audio.file_name:
            orig_name = audio.file_name.split("?", 1)[0]
        elif audio.title:
            orig_name = f"{audio.title}.mp3"
        else:
            orig_name = f"{audio.file_unique_id}.mp3"

        safe_name = sanitize(orig_name)
        local_path = user_dir / safe_name

        await msg.bot.download_file(file.file_path, destination=str(local_path))

        # запись в БД
        session.add(AudioFile(
            owner_id=user.id,
            file_id=audio.file_id,
            file_unique_id=audio.file_unique_id,
            file_path=str(local_path),
            display_name=orig_name,
            title=audio.title,
            duration=audio.duration,
        ))
        await session.commit()

    await msg.answer("✅ Сохранил! Позже сможешь слушать в веб-плеере.")
