"""Routes for user-related operations."""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import JSONResponse
from backend.storage.database import get_db
from backend.storage.pre_populated.seed_lists import ITEM_CATEGORIES
from backend.models.item_category import ItemCategory

categories_router = APIRouter(prefix="/categories", tags=["categories"])


@categories_router.get("/all", status_code=status.HTTP_200_OK)
def add_user(db=Depends(get_db)):
    """Get all item categories the database."""
    categories = db.query(ItemCategory).all()
    if not categories:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No categories found."},
        )

    return JSONResponse(
        content={"categories": [category.to_dict() for category in categories]}
    )
