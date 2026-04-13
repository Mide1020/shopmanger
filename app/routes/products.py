from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, PaginatedProductResponse
from app.utils.dependencies import admin_only
from app.services import product_service
from typing import Optional
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache
from app.utils.rate_limit import limiter

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=ProductResponse)
@limiter.limit("20/minute")
async def create_product(request: Request, product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    result = product_service.create_product(db, product)
    await FastAPICache.clear(namespace="products")
    return result

@router.get("/", response_model=PaginatedProductResponse)
@cache(expire=60, namespace="products")
@limiter.limit("60/minute")
def get_products(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
    return product_service.get_all_products(db, page, limit, search, category)

@router.get("/{product_id}", response_model=ProductResponse)
@cache(expire=60, namespace="products")
@limiter.limit("60/minute")
def get_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
@limiter.limit("20/minute")
async def update_product(request: Request, product_id: int, updated: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    result = product_service.update_product(db, product_id, updated)
    await FastAPICache.clear(namespace="products")
    return result

@router.delete("/{product_id}")
@limiter.limit("20/minute")
async def delete_product(request: Request, product_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    product_service.delete_product(db, product_id)
    await FastAPICache.clear(namespace="products")
    return {"message": "Product deleted successfully"}