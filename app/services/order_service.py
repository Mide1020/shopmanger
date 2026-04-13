from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderUpdate
from app.crud import order as crud_order
from app.crud import product as crud_product
from app.logger import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)

def process_order(db: Session, order: OrderCreate):
    logger.info(f"Processing order for customer id: {order.customer_id}")

    try:
        # The atomic stock decrement and order creation happens inside crud_order.create_order
        new_order = crud_order.create_order(db, order)
        db.commit()
        db.refresh(new_order)
        logger.info(f"Order processed successfully with id: {new_order.id}")

        # Check for low stock alerts after successful commit
        for item in new_order.items:
            if item.product.stock <= item.product.low_stock_threshold:
                logger.warning(f"Low stock alert! Product: {item.product.name} stock: {item.product.stock}")

        return new_order
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to process order: {str(e)}")
        raise e

def get_order(db: Session, order_id: int):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_all_orders(db: Session):
    return crud_order.get_all_orders(db)

def update_order(db: Session, order_id: int, updated: OrderUpdate):
    try:
        order = crud_order.update_order(db, order_id, updated)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise e

def delete_order(db: Session, order_id: int):
    try:
        order = crud_order.delete_order(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        db.commit()
        return order
    except Exception as e:
        db.rollback()
        raise e