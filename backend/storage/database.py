"""Database connection and session logic"""

import os
import logging
from pathlib import Path
from pydantic import Field
from pydantic_settings import SettingsConfigDict
from typing import Optional, Generator
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, Session, sessionmaker

# models import
from . import Base
from backend.models.user import User

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class DatabaseSettings(BaseSettings):
    """Database configuration settings"""

    # required
    user: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")

    # optionals with defaults
    host: str = Field("localhost", description="Database hostname")
    port: int = Field(5432, description="Database port")
    name: str = Field("app_template_db", description="Database name")

    # connection settings
    pool_size: int = Field(10, description="Number of connections in the pool")
    max_overflow: int = Field(
        10, description="Number of extra connections when the pool is full"
    )
    pool_recycle: int = Field(
        3600, description="Time in seconds to recycle connections"
    )
    pool_pre_ping: bool = Field(True, description="Check connections before using them")

    model_config = SettingsConfigDict(
        env_prefix="DB_",  # Prefix for db-related environment variables
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",  # Allow extra fields in the settings
    )

    @property
    def db_url(self) -> str:
        """Construct the database URL from db settings."""

        return (
            f"postgresql+psycopg2://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )


db_settings = DatabaseSettings()  # type: ignore


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
