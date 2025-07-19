import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables
from api import router as api_router
from bot.main import setup_bot
import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Dunya Jewellery Bot...")

    # Create database tables
    create_tables()
    print("📊 Database tables created")

    # Setup and start bot
    bot_app = setup_bot()
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    print("🤖 Telegram bot started")

    yield

    # Shutdown
    await bot_app.updater.stop()
    await bot_app.stop()
    await bot_app.shutdown()
    print("🛑 Bot stopped")


# Create FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    description="E-commerce API with Telegram Bot Admin",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
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
    return {"message": "Dunya Jewellery API", "status": "running"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )