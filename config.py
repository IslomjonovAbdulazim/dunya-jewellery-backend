import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_IDS = [int(id.strip()) for id in os.getenv("ADMIN_CHAT_ID", "").split(",") if id.strip()]

# Database Configuration
# Primary: Use DATABASE_URL directly
DATABASE_URL = os.getenv("DATABASE_URL")

# Alternative: Individual database components (fallback)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# App Configuration
APP_NAME = os.getenv("APP_NAME", "Dunya Jewellery Bot")

# Print configuration for debugging
if DEBUG:
    print("🔧 Configuration:")
    print(f"  - Database: {'PostgreSQL' if DATABASE_URL and 'postgresql' in DATABASE_URL else 'SQLite'}")
    print(f"  - Debug Mode: {DEBUG}")
    print(f"  - Admin IDs: {ADMIN_CHAT_IDS}")
    print(f"  - App Name: {APP_NAME}")