from sqlalchemy.orm import Session
from typing import List

from hashiramart.api.schemas.product_schema import ProductCreate, ProductUpdate
from hashiramart.infrastructure.database.model.product import Product
from hashiramart.infrastructure.database.repositories.base_repo import BaseRepository


# The import path now points to the new 'product_schema.py' file.


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    """
    Repository for all database operations related to the Product model.
    """
    def filter_by_category(self, db: Session, *, category: str) -> List[Product]:
        """
        Retrieves all products belonging to a specific category.

        :param db: The database session.
        :param category: The category name to filter by.
        :return: A list of Product instances.
        """
        return db.query(Product).filter(Product.category == category).all()

