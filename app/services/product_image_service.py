from sqlalchemy.orm import Session
from app.schemas.product_image import ProductImageCreate
from app.crud import product_image as crud_image
from app.crud import product as crud_product
from app.logger import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)

def add_image(db: Session, product_id: int, image: ProductImageCreate):
    product = crud_product.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Adding image to product id: {product_id}")
    new_image = crud_image.add_product_image(db, product_id, image)
    db.commit()
    db.refresh(new_image)
    logger.info(f"Image added successfully to product: {product.name}")
    return new_image

def get_images(db: Session, product_id: int):
    product = crud_product.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud_image.get_product_images(db, product_id)

def delete_image(db: Session, image_id: int):
    image = crud_image.delete_product_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.commit()
    logger.info(f"Image deleted successfully: {image_id}")
    return image