import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get("TOKEN")
API_ID: str = os.environ.get("API_ID")
API_HASH: str = os.environ.get("API_HASH")
OWNER: int = int(os.environ.get("OWNER"))
DATABASE_URL: str = os.environ.get("DATABASE_URL")
# códigos de los idiomas habilitados en el bot
# en orden con "change_translate" de languages.py
lang_code = ["es", "en", "hi", "ar", "pt", "ru", "fr"]
