from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate
from fastapi import HTTPException

def create_order(db: Session, order: OrderCreate):
    total = 0
    order_items = []

    # Sort items by product_id to prevent deadlocks when acquiring row-level locks
    sorted_items = sorted(order.items, key=lambda i: i.product_id)

    for item in sorted_items:
        # Use with_for_update() to lock the product row and prevent race conditions
        product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

        total += product.price * item.quantity
        product.stock -= item.quantity

        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        ))

    new_order = Order(
        customer_id=order.customer_id,
        total=total,
        payment_status=order.payment_status
    )
    db.add(new_order)
    db.flush()

    for item in order_items:
        item.order_id = new_order.id
        db.add(item)

    # We skip db.commit() here to allow service layer to manage the transaction
    db.flush() 
    return new_order

def get_all_orders(db: Session):
    return db.query(Order).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order(db: Session, order_id: int, updated: OrderUpdate):
    order = get_order_by_id(db, order_id)
    if order:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(order, key, value)
        db.flush()
    return order

def delete_order(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.flush()
    return order