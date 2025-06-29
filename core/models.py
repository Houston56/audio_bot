from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
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
    file_path  = Column(String, nullable=False)      # локальный путь
    title      = Column(String(255))
    duration   = Column(Integer)                     # секунды
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="audios")