"""Database configuration"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


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
        env_file=Path(__file__).parent.parent.parent / ".env",
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
