from sqlalchemy.orm import Session
from typing import Optional

from hashiramart.api.schemas.user_schema import UserCreate, UserUpdate
from hashiramart.infrastructure.database.model.user import User
from hashiramart.infrastructure.database.repositories.base_repo import BaseRepository
from hashiramart.security.hashing import Hasher


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    Repository for all database operations related to the User model.
    """

    def get_by_name(self, db: Session, *, name: str) -> Optional[User]:
        """
        Retrieves a user by their name.

        :param db: The database session.
        :param name: The name of the user.
        :return: The User instance or None if not found.
        """
        return db.query(User).filter(User.name == name).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Creates a new user, hashing the password before saving.

        :param db: The database session.
        :param obj_in: The Pydantic schema with the user creation data.
        :return: The newly created User instance.
        """
        # Convert Pydantic schema to a dictionary
        create_data = obj_in.model_dump()

        # Hash the password using the Hasher utility
        create_data["hashed_password"] = Hasher.get_password_hash(create_data["password"])

        # Remove the plain password from the dictionary before creating the model
        del create_data["password"]

        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, name: str, password: str) -> Optional[User]:
        """
        Authenticates a user by checking their name and password.

        :param db: The database session.
        :param name: The username.
        :param password: The plain text password.
        :return: The User instance if authentication is successful, otherwise None.
        """
        # Find the user by their name
        user = self.get_by_name(db, name=name)
        if not user:
            return None

        # Verify the provided password against the stored hash
        if not Hasher.verify_password(password, user.hashed_password):
            return None

        return user


