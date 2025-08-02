from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.storage import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), nullable=False)

    def to_dict(self):
        """Convert Role instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        """String representation of Role instance."""
        return f"<Role(id={self.id}, name='{self.name}')>"
