from pydantic import BaseModel
from typing import Optional

# --- Base Schema ---
# Common attributes for a user. Note the absence of the password.
class UserBase(BaseModel):
    name: str
    breathing_style: Optional[str] = None
    level: Optional[int] = None

# --- Create Schema ---
# Used when creating a new user. It's the only schema that includes the password.
class UserCreate(UserBase):
    password: str

# --- Update Schema ---
# Used for updating a user's profile.
class UserUpdate(BaseModel):
    breathing_style: Optional[str] = None
    level: Optional[int] = None

# --- Read Schema ---
# This is the schema for returning user data from the API.
# It NEVER includes the hashed_password for security.
class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True