from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN_I")
API_KEY = os.getenv("API_KEY_I")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found in .env")

if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY not found in .env")

