from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime as dt, timezone as tz
from backend.storage import Base


# example user model
class User(Base):
    __tablename__ = "users"

    id = Column(
        String(6), primary_key=True, index=True, nullable=False
    )  # predefined student ID
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(
        self, id: str, first_name: str, last_name: str, email: str, hashed_password: str
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password
        self.created_at = self.updated_at = dt.now(tz.utc)
        self.created_at = self.updated_at = dt.now(tz.utc)

    def to_dict(self):
        """Convert User instance to dictionary."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        """String representation of User instance."""
        return (
            f"<User(id={self.id}, first_name='{self.first_name}', "
            f"last_name='{self.last_name}', email='{self.email}')>"
        )
