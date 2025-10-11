from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from hashiramart.api.schemas.auth_schema import Token
from hashiramart.infrastructure.database.connection import get_db
from hashiramart.infrastructure.database.repositories.user_repo import UserRepository
from hashiramart.security.authentication import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
    Authenticates a user and returns a JWT access token.
    """
    # 1. Use the user repository to authenticate the user with the provided credentials
    user_repo = UserRepository()
    user = user_repo.authenticate(
        db, name=form_data.username, password=form_data.password
    )

    # 2. If authentication fails, raise an error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. If authentication is successful, create an access token
    # The 'sub' (subject) of the token is the user's unique identifier (their name)
    access_token = create_access_token(data={"sub": user.name})

    # 4. Return the token
    return {"access_token": access_token, "token_type": "bearer"}