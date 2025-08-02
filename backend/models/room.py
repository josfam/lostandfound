from sqlalchemy import Column, Integer, String, Text
from backend.storage import Base


class Room(Base):
    """Represents a room in the institution."""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(60), nullable=False)

    def __init__(self, code: str):
        self.code = code

    def to_dict(self):
        """Convert Room instance to dictionary."""
        return {
            "id": self.id,
            "code": self.code,
        }

    def __repr__(self):
        """String representation of Room instance."""
        return f"<Room(id={self.id}, code='{self.code}')>"
