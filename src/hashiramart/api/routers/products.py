from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from hashiramart.api.schemas.product_schema import ProductSchema, ProductCreate, ProductUpdate
from hashiramart.infrastructure.database.connection import get_db
from hashiramart.infrastructure.database.repositories.product_repo import ProductRepository

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    product_repo = ProductRepository()
    return product_repo.create(db=db, obj_in=product)

@router.get("/", response_model=List[ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all products with pagination.
    """
    product_repo = ProductRepository()
    products = product_repo.get_all(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single product by its ID.
    """
    product_repo = ProductRepository()
    db_product = product_repo.get(db, obj_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """
    Update an existing product.
    """
    product_repo = ProductRepository()
    db_product = product_repo.get(db, obj_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_repo.update(db=db, db_obj=db_product, obj_in=product)

@router.delete("/{product_id}", response_model=ProductSchema)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product.
    """
    product_repo = ProductRepository()
    db_product = product_repo.get(db, obj_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_repo.remove(db=db, obj_id=product_id)