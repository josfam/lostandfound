from sqlalchemy import Column, Integer, String
from backend.storage import Base


class ItemCategory(Base):
    __tablename__ = "item_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), nullable=False)

    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        """Convert Role instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        """String representation of ItemCategory instance."""
        return f"<ItemCategory(id={self.id}, name='{self.name}')>"
