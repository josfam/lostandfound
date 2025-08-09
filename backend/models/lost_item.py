from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from datetime import datetime as dt, timezone as tz
from backend.storage import Base
from typing import Optional
from backend.api.utils.constants import ItemStatus


class LostItem(Base):
    """Represents a lost item in the institution."""

    __tablename__ = "lost_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    description = Column(String(500), nullable=True, default="No description provided")
    image_url = Column(String(255), nullable=True, default="")
    status = Column(
        Enum(ItemStatus, name="item_status"),
        nullable=False,
        default=ItemStatus.DROPPED_OFF.value,
    )
    found_by = Column(
        String(6), ForeignKey("users.id"), nullable=False
    )  # The student who found the lost item
    dropped_off_by = Column(
        String(6), ForeignKey("users.id"), nullable=True
    )  # The student who dropped off the item
    found_in = Column(Integer, ForeignKey("rooms.id"), nullable=False, default=-1)
    claimed_by = Column(String(6), ForeignKey("users.id"), nullable=True)
    collected_by = Column(String(6), ForeignKey("users.id"), nullable=True)
    dropped_off_at = Column(
        Integer, ForeignKey("drop_off_locations.id"), nullable=False, default=-1
    )
    category = Column(Integer, ForeignKey("item_categories.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=dt.now(tz.utc))
    updated_at = Column(DateTime, nullable=False, default=dt.now(tz.utc))

    def __init__(
        self,
        *,
        name: str,
        description: str = "No description provided",
        image_url: str = "",
        status: str = "dropped off",
        found_by: str,
        dropped_off_by: Optional[str] = None,
        found_in: int,
        claimed_by: Optional[str] = None,
        collected_by: Optional[str] = None,
        dropped_off_at: Optional[int] = None,
        category: int,
    ):
        self.name = name
        self.description = description
        self.image_url = image_url
        self.status = status
        self.found_by = found_by
        self.dropped_off_by = dropped_off_by
        self.found_in = found_in
        self.claimed_by = claimed_by
        self.collected_by = collected_by
        self.dropped_off_at = dropped_off_at
        self.category = category
        self.created_at = dt.now(tz.utc)
        self.updated_at = dt.now(tz.utc)

    def to_dict(self):
        """Convert LostItem instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "status": self.status,
            "found_by": self.found_by,
            "dropped_off_by": self.dropped_off_by,
            "found_in": self.found_in,
            "claimed_by": self.claimed_by,
            "collected_by": self.collected_by,
            "dropped_off_at": self.dropped_off_at,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
