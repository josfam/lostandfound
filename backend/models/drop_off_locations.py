from sqlalchemy import Column, Integer, String, Text
from backend.storage import Base


class DropOffLocation(Base):
    __tablename__ = "drop_off_locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=False, default="No description provided")

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_dict(self):
        """Convert DropOffLocation instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    def __repr__(self):
        """String representation of DropOffLocation instance."""
        return f"<DropOffLocation(id={self.id}, name='{self.name}, description='{self.description}')>"
