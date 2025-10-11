from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from hashiramart.infrastructure.database.connection import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)
    material = Column(String, nullable=True)

    # Use a string "Interaction" to prevent circular imports
    interactions = relationship("Interaction", back_populates="product")