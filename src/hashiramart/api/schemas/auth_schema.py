from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """
    Schema for the access token returned on successful login.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for the data encoded within the JWT.
    """
    username: Optional[str] = None