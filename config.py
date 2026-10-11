import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
DEFAULT_LANG: str = os.getenv("DEFAULT_LANG", "id")
MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "2000"))
MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "100"))
DB_PATH: str = os.getenv("DB_PATH", "translator.db")
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
ADMIN_IDS: list[int] = [
    int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
]
