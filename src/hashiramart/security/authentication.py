from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from google.auth import jwt
from jose import JWTError
from sqlalchemy.orm import Session


from hashiramart.api.schemas.auth_schema import TokenData
from hashiramart.config.settings import settings
from hashiramart.infrastructure.database.connection import get_db
from hashiramart.infrastructure.database.repositories.user_repo import UserRepository

# This tells FastAPI where the client should go to get a token.
# The URL "/auth/token" must match the endpoint we'll create in the auth router.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a new JWT access token.

    :param data: The data to encode in the token (e.g., username).
    :param expires_delta: The lifespan of the token.
    :return: The encoded JWT string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration time from settings
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    A FastAPI dependency to decode and verify a token, then return the current user.
    This function will be used to protect routes.

    :param token: The JWT token from the request's Authorization header.
    :param db: The database session.
    :return: The user model instance if the token is valid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # Validate the data with our Pydantic model
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    # Fetch the user from the database
    user_repo = UserRepository()
    user = user_repo.get_by_name(db, name=token_data.username)
    if user is None:
        raise credentials_exception

    return user