from sqlalchemy.orm import Session
from app.models.product_image import ProductImage
from app.schemas.product_image import ProductImageCreate

def add_product_image(db: Session, product_id: int, image: ProductImageCreate):
    # If this image is primary, unset all other primary images for this product
    if image.is_primary:
        db.query(ProductImage).filter(
            ProductImage.product_id == product_id,
            ProductImage.is_primary == True
        ).update({"is_primary": False})
        db.flush()

    new_image = ProductImage(
        product_id=product_id,
        image_url=image.image_url,
        is_primary=image.is_primary
    )
    db.add(new_image)
    db.flush()
    return new_image

def get_product_images(db: Session, product_id: int):
    return db.query(ProductImage).filter(ProductImage.product_id == product_id).all()

def delete_product_image(db: Session, image_id: int):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if image:
        db.delete(image)
        db.flush()
    return image