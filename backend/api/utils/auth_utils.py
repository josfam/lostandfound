"""Authentication utilities for the backend API."""

import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    if not isinstance(password, str):
        raise ValueError("Password must be a string.")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def password_matches(hashed_password: str, password: str) -> bool:
    """Check if a password matches the hashed password."""
    if not isinstance(hashed_password, str) or not isinstance(password, str):
        raise ValueError("Both hashed_password and password must be strings.")
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_default_password(email: str = "", first_name: str = "") -> str:
    """Generate a default password for new users."""
    if not email or not first_name:
        raise ValueError(
            "`Email` and `first name` must be provided for a default password."
        )
    return f"{first_name.lower()}_{email.split('@')[0]}_default"
