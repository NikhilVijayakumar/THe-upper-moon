from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from hashiramart.infrastructure.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    breathing_style = Column(String, nullable=True)
    level = Column(Integer, default=1)

    # Use a string "Interaction" to prevent circular imports
    interactions = relationship("Interaction", back_populates="user")