"""Routes for user-related operations."""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import JSONResponse
from backend.storage.database import get_db
from backend.models.user import User
from backend.api.utils.auth_utils import hash_password, generate_default_password
from backend.storage.pre_populated import USER_ROLES

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/add", status_code=status.HTTP_201_CREATED)
def add_user(user: dict = Body(...), db=Depends(get_db)):
    """Add a new user to the database."""
    role_name: str = user.get("role_name", "").strip()
    if role_name.lower() not in USER_ROLES:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": f"Invalid role name: {role_name}. Valid roles are: {', '.join(USER_ROLES)}."
            },
        )
    id: str = user.get("id", "").strip()
    first_name: str = user.get("first_name", "").strip()
    last_name: str = user.get("last_name", "").strip()
    email: str = user.get("email", "").strip()

    if not all([id, first_name, last_name, email]):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "First name, last name, and email are required."},
        )

    # create user
    user = User(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=generate_default_password(email=email, first_name=first_name),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return JSONResponse(
            content={"message": "User added successfully", "user_id": user.id}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An error occurred while adding the user."},
        )


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
