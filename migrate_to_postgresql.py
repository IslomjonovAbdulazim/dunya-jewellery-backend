"""
Initialize or reset the PostgreSQL database for Dunya Jewellery.

Usage:
  - Create/upgrade tables (non-destructive):
      ./.venv/bin/python migrate_to_postgresql.py

  - Drop and recreate all tables (DESTRUCTIVE):
      ./.venv/bin/python migrate_to_postgresql.py --reset
"""

import sys
from typing import Optional

from sqlalchemy import text

import config  # loads .env
from database import engine, create_tables
from models import Base, Contact
from database import get_db_session


def test_db_connection() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Connected to database")
        return True
    except Exception as exc:
        print(f"❌ Failed to connect: {exc}")
        return False


def reset_db():
    print("⚠️ Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped")


def init_tables_and_seed():
    print("📦 Creating tables...")
    create_tables()

    # Seed default contact if none exists
    db = get_db_session()
    try:
        has_contact = db.query(Contact).count() > 0
        if not has_contact:
            contact = Contact(
                telegram_username="dunya_jewellery",
                phone_numbers="+998901234567",
                instagram_username="dunya_jewellery",
                is_active=True,
            )
            db.add(contact)
            db.commit()
            print("🌱 Seeded default contact")
    finally:
        db.close()

    print("✅ Tables ready")


def main(argv: Optional[list] = None):
    argv = argv or sys.argv[1:]
    do_reset = "--reset" in argv

    print("🔧 Using DATABASE:")
    print(f"   {config.DATABASE_URL}")

    if not test_db_connection():
        sys.exit(1)

    if do_reset:
        reset_db()

    init_tables_and_seed()


if __name__ == "__main__":
    main()


