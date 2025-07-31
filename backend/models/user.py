from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from backend.storage import Base


# example user model
class User(Base):
    __tablename__ = "users"

    id = Column(String(6), primary_key=True, index=True)  # predefined student ID
    first_name = Column(String(120), unique=True)
    last_name = Column(String(120), unique=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def to_dict(self):
        """Convert User instance to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
