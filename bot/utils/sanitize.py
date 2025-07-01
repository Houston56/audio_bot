import re
SAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]")

def sanitize(name: str, limit: int = 120) -> str:
    """Убираем пробелы/кириллицу/спецсимволы → '_' и обрезаем длину."""
    return SAFE_CHARS.sub("_", name)[:limit]