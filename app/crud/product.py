from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from typing import Optional
from datetime import datetime, timezone

def create_product(db: Session, product: ProductCreate):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.flush()
    return new_product

def get_all_products(db: Session, page: int = 1, limit: int = 10, search: Optional[str] = None, category: Optional[str] = None):
    query = db.query(Product).filter(Product.is_active == True, Product.deleted_at.is_(None))

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))

    total = query.count()
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": -(-total // limit) if limit > 0 else 0,  # ceiling division
        "items": items,
    }

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id, Product.deleted_at.is_(None)).first()

def update_product(db: Session, product_id: int, updated: ProductUpdate):
    product = get_product_by_id(db, product_id)
    if product:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        db.flush()
    return product

def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if product:
        product.deleted_at = datetime.now(timezone.utc)
        product.is_active = False # Safely mark as inactive as well
        db.flush()
    return product

def get_low_stock_products(db: Session):
    return db.query(Product).filter(
        Product.stock <= Product.low_stock_threshold,
        Product.is_active == True,
        Product.deleted_at.is_(None)
    ).all()

def update_stock(db: Session, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.id == product_id, Product.deleted_at.is_(None)).with_for_update().first()
    if product:
        if product.stock + quantity < 0:
            raise ValueError("Stock cannot be negative")
        product.stock += quantity
        db.flush()
    return product