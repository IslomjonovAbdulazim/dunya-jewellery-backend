import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables, test_connection
from api import router as api_router
from bot.main import setup_bot
import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Dunya Jewellery Bot...")

    # Test database connection
    print("🔍 Testing database connection...")
    if not test_connection():
        print("❌ Database connection failed! Please check your configuration.")
        print("💡 Troubleshooting tips:")
        print("   1. Check your DATABASE_URL in .env file")
        print("   2. Make sure PostgreSQL server is running")
        print("   3. Verify credentials and network connectivity")
        print("   4. Try running: python migrate_to_postgresql.py")
        raise Exception("Database connection failed")

    # Create database tables
    try:
        create_tables()
        print("📊 Database ready")
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        raise

    # Setup and start bot (optional if BOT_TOKEN is configured)
    bot_app = None
    try:
        if getattr(config, 'BOT_TOKEN', None):
            bot_app = setup_bot()
            await bot_app.initialize()
            await bot_app.start()
            await bot_app.updater.start_polling()
            print("🤖 Bot started successfully")
        else:
            print("⚠️  BOT_TOKEN not set — starting API without Telegram bot")
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        raise

    yield

    # Shutdown
    try:
        if bot_app is not None:
            await bot_app.updater.stop()
            await bot_app.stop()
            await bot_app.shutdown()
            print("🛑 Bot stopped")
    except Exception as e:
        print(f"⚠️ Error during shutdown: {e}")


# Create FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    description="Jewelry E-commerce API with Telegram Bot (PostgreSQL)",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Dunya Jewellery API",
        "status": "running",
        "database": "PostgreSQL" if config.DATABASE_URL and "postgresql" in config.DATABASE_URL else "SQLite"
    }


@app.get("/health")
async def health_check():
    """Enhanced health check with database status"""
    try:
        db_status = test_connection()
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database": "PostgreSQL" if config.DATABASE_URL and "postgresql" in config.DATABASE_URL else "SQLite",
            "database_connected": db_status
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    print("🌟 Dunya Jewellery Bot with PostgreSQL")
    print("=" * 40)

    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )