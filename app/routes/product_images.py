from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product_image import ProductImageCreate, ProductImageResponse
from app.utils.dependencies import admin_only
from app.services import product_image_service
from typing import List

router = APIRouter(
    prefix="/products/{product_id}/images",
    tags=["Product Images"]
)

# ADD IMAGE TO PRODUCT (admin only)
@router.post("/", response_model=ProductImageResponse)
def add_image(product_id: int, image: ProductImageCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return product_image_service.add_image(db, product_id, image)

# GET ALL IMAGES FOR A PRODUCT (anyone)
@router.get("/", response_model=List[ProductImageResponse])
def get_images(product_id: int, db: Session = Depends(get_db)):
    return product_image_service.get_images(db, product_id)

# DELETE AN IMAGE (admin only)
@router.delete("/{image_id}")
def delete_image(product_id: int, image_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    product_image_service.delete_image(db, image_id)
    return {"message": "Image deleted successfully"}