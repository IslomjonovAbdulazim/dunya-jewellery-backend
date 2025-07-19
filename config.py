import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_IDS = [int(id.strip()) for id in os.getenv("ADMIN_CHAT_ID", "").split(",") if id.strip()]

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# App
APP_NAME = os.getenv("APP_NAME", "Dunya Jewellery Bot")