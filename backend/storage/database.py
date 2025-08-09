"""Database connection and session logic"""

import os
import csv
import logging
from pathlib import Path
from pydantic import Field
from typing import Optional, Generator
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from backend.storage.pre_populated.seed_lists import USER_ROLES, ITEM_CATEGORIES
from backend.api.config.db_config import DatabaseSettings, db_settings

# models import
from . import Base
from backend.models.user import User
from backend.models.role import Role
from backend.models.room import Room
from backend.models.drop_off_locations import DropOffLocation
from backend.models.item_category import ItemCategory
from backend.models.lost_item import LostItem

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def make_db_engine(settings: Optional[DatabaseSettings] = None) -> Engine:
    """Create the database engine with given settings."""

    if settings is None:
        settings = db_settings

    try:
        # create the engine
        engine = create_engine(
            url=settings.db_url,
            pool_size=settings.pool_size,
            max_overflow=settings.max_overflow,
            pool_recycle=settings.pool_recycle,
            pool_pre_ping=settings.pool_pre_ping,
            echo=os.getenv("DB_ECHO", "False").lower() == "true",
        )
        # test the connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Test database connection successful!.")
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        raise e
    else:
        logger.info("Database engine created successfully.")
        return engine


# Global engine
engine: Optional[Engine] = None
sessionLocal: Optional[sessionmaker] = None


def db_init(settings: Optional[DatabaseSettings] = None):
    """Initialize the database connection."""
    global engine, sessionLocal

    if settings is None:
        settings = db_settings

    try:
        engine = make_db_engine(settings)
        sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        # drop tables if DROP_TABLES_FIRST is set
        if os.getenv("DROP_TABLES_FIRST", "0") == "1":
            Base.metadata.drop_all(bind=engine)
            logger.info("Dropped all tables as per DROP_TABLES_FIRST setting.")
        Base.metadata.create_all(bind=engine)  # Create tables if they don't exist
    except SQLAlchemyError as e:
        logger.error(f"Failed to initialize database connection: {e}")
        raise e

    logger.info("Database initialized...")


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    global sessionLocal
    if not sessionLocal:
        raise Exception("Database not initialized. Call db_init() first.")

    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


def pre_populate_user_roles():
    """Pre-populate user roles in the database."""
    global sessionLocal

    if not sessionLocal:
        raise Exception("Database not initialized. Call db_init() first.")

    with sessionLocal() as session:
        for role_name in USER_ROLES:
            existing_role = session.query(Role).filter_by(name=role_name).first()
            if not existing_role:
                new_role = Role(name=role_name)
                session.add(new_role)
        session.commit()
        logger.info("User roles pre-populated successfully.")


def pre_populate_item_categories():
    """Pre-populate categories in the database."""
    global sessionLocal

    if not sessionLocal:
        raise Exception("Database not initialized. Call db_init() first.")

    with sessionLocal() as session:
        # Example categories, replace with actual categories as needed
        for category_name in ITEM_CATEGORIES:
            existing_category = (
                session.query(ItemCategory).filter_by(name=category_name).first()
            )
            if not existing_category:
                new_category = ItemCategory(name=category_name)
                session.add(new_category)
        session.commit()
        logger.info("Categories pre-populated successfully.")


def pre_populate_drop_off_locations():
    """Pre-populate drop-off locations in the database."""
    global sessionLocal

    if not sessionLocal:
        raise Exception("Database not initialized. Call db_init() first.")

    drop_off_file = Path(__file__).parent / "pre_populated" / "dropofflocations.csv"
    with open(drop_off_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with sessionLocal() as session:
            for row in reader:
                name: str = row.get("name", "").strip()
                description: str = row.get("description", "").strip()

                if not name:
                    logger.warning("Skipping drop-off location with empty name.")
                    continue

                existing_location = (
                    session.query(DropOffLocation).filter_by(name=name).first()
                )
                if not existing_location:
                    new_location = DropOffLocation(name=name, description=description)
                    session.add(new_location)
            session.commit()
            logger.info("Drop-off locations pre-populated successfully.")


def pre_populate_rooms():
    """Pre-populate rooms in the database."""
    global sessionLocal

    if not sessionLocal:
        raise Exception("Database not initialized. Call db_init() first.")

    rooms_file = Path(__file__).parent / "pre_populated" / "rooms.csv"
    with open(rooms_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with sessionLocal() as session:
            for row in reader:
                room_code: str = row.get("room code", "").strip()
                if not room_code:
                    logger.warning("Skipping room with empty code.")
                    continue

                existing_room = session.query(Room).filter_by(code=room_code).first()
                if not existing_room:
                    new_room = Room(code=room_code)
                    session.add(new_room)
            session.commit()
            logger.info("Rooms pre-populated successfully.")


def pre_populate_tables():
    """Pre-populate tables in the database."""
    pre_populate_user_roles()
    pre_populate_item_categories()
    pre_populate_drop_off_locations()
    pre_populate_rooms()
    logger.info("Pre-population of tables completed successfully.")


def close_db():
    """Close the database connection."""
    global engine, sessionLocal

    if engine:
        try:
            engine.dispose()
            logger.info("Database connection closed.")
        except SQLAlchemyError as e:
            logger.error(f"Error closing database connection: {e}")
    else:
        logger.warning("No database connection to close.")

    engine = None
    sessionLocal = None
