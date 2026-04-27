from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate
from app.crud import product as crud_product
from app.logger import get_logger
from fastapi import HTTPException
from typing import Optional

logger = get_logger(__name__)

def create_product(db: Session, product: ProductCreate):
    logger.info(f"Creating product: {product.name}")
    try:
        new_product = crud_product.create_product(db, product)
        db.commit()
        db.refresh(new_product)
        logger.info(f"Product created successfully: {new_product.name}")
        return new_product
    except Exception as e:
        db.rollback()
        raise e

def get_all_products(db: Session, page: int = 1, limit: int = 10, search: Optional[str] = None, category: Optional[str] = None):
    logger.info(f"Fetching products - page: {page}, limit: {limit}, search: {search}, category: {category}")
    return crud_product.get_all_products(db, page, limit, search, category)

def get_product(db: Session, product_id: int):
    product = crud_product.get_product_by_id(db, product_id)
    if not product:
        logger.warning(f"Product not found with id: {product_id}")
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product(db: Session, product_id: int, updated: ProductUpdate):
    try:
        product = crud_product.update_product(db, product_id, updated)
        if not product:
            logger.warning(f"Product not found with id: {product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise e

def delete_product(db: Session, product_id: int):
    try:
        product = crud_product.delete_product(db, product_id)
        if not product:
            logger.warning(f"Product not found with id: {product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        db.commit()
        return product
    except Exception as e:
        db.rollback()
        raise e

def get_low_stock(db: Session):
    logger.info("Checking low stock products")
    return crud_product.get_low_stock_products(db)

def update_stock(db: Session, product_id: int, quantity: int):
    try:
        updated = crud_product.update_stock(db, product_id, quantity)
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.commit()
        db.refresh(updated)
        
        if updated.stock <= updated.low_stock_threshold:
            logger.warning(f"Low stock alert! Product: {updated.name} stock: {updated.stock}")
        
        return updated
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise e