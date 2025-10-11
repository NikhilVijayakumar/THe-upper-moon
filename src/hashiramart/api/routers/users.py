from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from hashiramart.api.schemas.user_schema import UserSchema, UserCreate
from hashiramart.infrastructure.database.connection import get_db
from hashiramart.infrastructure.database.repositories.user_repo import UserRepository
from hashiramart.security.authentication import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user (signup).
    """
    user_repo = UserRepository()
    db_user = user_repo.get_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_repo.create(db=db, obj_in=user)

@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    """
    Get the profile for the currently authenticated user.
    """
    # The `get_current_user` dependency handles token validation and fetching the user.
    # We just need to return it.
    return current_user