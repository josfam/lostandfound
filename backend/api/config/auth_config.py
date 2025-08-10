from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


class AuthConfig(BaseSettings):
    """Authentication configuration settings"""

    # required
    jwt_secret_key: str = Field(..., description="Secret key for signing tokens")
    jwt_algorithm: str = Field("HS256", description="Algorithm used for token signing")
    jwt_expiration_time: int = Field(
        3600, description="JWT token expiration time in minutes"
    )

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",  # Prefix for auth-related environment variables
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",  # Allow extra fields in the settings
    )


auth_config = AuthConfig()  # type: ignore
