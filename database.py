from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from models import Base
import config
import os


# PostgreSQL connection with proper configuration
def get_database_url():
    """Get database URL with fallback options"""

    # Option 1: Use direct DATABASE_URL from .env
    if config.DATABASE_URL:
        url = config.DATABASE_URL
        # Normalize common Heroku-style URL prefix
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)

        # Append sslmode for managed providers (e.g., Railway) unless already specified
        if url.startswith("postgresql://") and "sslmode=" not in url:
            sslmode = getattr(config, 'DB_SSLMODE', None) or "require"
            separator = '&' if '?' in url else '?'
            url = f"{url}{separator}sslmode={sslmode}"
        return url

    # Option 2: Build from individual components (if DATABASE_URL doesn't work)
    if hasattr(config, 'DB_HOST') and config.DB_HOST:
        return f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

    # Fallback to SQLite for development
    return "sqlite:///./ecommerce.db"


# Create engine with PostgreSQL optimizations
database_url = get_database_url()

if database_url.startswith('postgresql'):
    # PostgreSQL configuration
    engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=config.DEBUG  # Show SQL queries in debug mode
    )
    print(f"✅ Connected to PostgreSQL database")
else:
    # SQLite configuration (fallback)
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        echo=config.DEBUG
    )
    print(f"⚠️  Using SQLite database (fallback)")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("📊 Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise


def test_connection():
    """Test database connection"""
    try:
        db = SessionLocal()
        # SQLAlchemy 2.0 requires textual SQL to be wrapped with text()
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection test successful")
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False


def get_db():
    """Get database session for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """Get database session for bot"""
    return SessionLocal()