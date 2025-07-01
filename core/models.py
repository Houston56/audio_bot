from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id           = Column(Integer, primary_key=True)
    tg_id        = Column(Integer, unique=True, nullable=False)
    username     = Column(String(64))
    first_name   = Column(String(64))
    last_name    = Column(String(64))
    created_at   = Column(DateTime, default=datetime.utcnow)

    audios = relationship("AudioFile", back_populates="owner")


class AudioFile(Base):
    __tablename__ = "audio_files"

    id         = Column(Integer, primary_key=True)
    owner_id   = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    file_id    = Column(String, nullable=False)      # Telegram FileID
    file_unique_id = Column(String,  nullable=False)
    file_path  = Column(String, nullable=False)
    title      = Column(String(255))
    duration   = Column(Integer)                     # секунды
    created_at = Column(DateTime, default=datetime.utcnow)
    display_name = Column(String(255))

    owner = relationship("User", back_populates="audios")

    __table_args__ = (
        # один и тот же файл не может повторяться у одного пользователя
        UniqueConstraint("owner_id", "file_unique_id", name="uix_owner_file"),
    )