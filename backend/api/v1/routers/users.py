"""Routes for user-related operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from backend.storage.database import get_db
from backend.models.user import User

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/count", status_code=status.HTTP_200_OK)
def get_user_count(db=Depends(get_db)):
    """Get the total number of users."""
    try:
        count = db.query(User).count()
        return JSONResponse(content={"user_count": count})
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An error occurred while fetching user count."},
        )
