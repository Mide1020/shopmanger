from fastapi import APIRouter, Depends, Query, Request, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, PaginatedOrderResponse
from app.utils.dependencies import admin_only
from app.services import order_service
from typing import List
from fastapi_cache import FastAPICache
from app.utils.rate_limit import limiter

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse)
@limiter.limit("20/minute")
async def create_order(request: Request, order: OrderCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    result = order_service.process_order(db, order, background_tasks)
    await FastAPICache.clear(namespace="products")
    return result

@router.get("/", response_model=PaginatedOrderResponse)
@limiter.limit("60/minute")
def get_orders(
    request: Request,
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db), 
    current_user = Depends(admin_only)
):
    return order_service.get_all_orders(db, page, limit)

@router.get("/{order_id}", response_model=OrderResponse)
@limiter.limit("60/minute")
def get_order(request: Request, order_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return order_service.get_order(db, order_id)

@router.put("/{order_id}", response_model=OrderResponse)
@limiter.limit("20/minute")
def update_order(request: Request, order_id: int, updated: OrderUpdate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return order_service.update_order(db, order_id, updated)

@router.delete("/{order_id}")
@limiter.limit("20/minute")
def delete_order(request: Request, order_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    order_service.delete_order(db, order_id)
    return {"message": "Order deleted successfully"}