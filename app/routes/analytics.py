from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.customer import Customer
from app.utils.dependencies import admin_only
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

# TOTAL REVENUE
@router.get("/revenue")
def get_total_revenue(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    total = db.query(func.sum(Order.total)).filter(Order.payment_status == "paid").scalar()
    return {"total_revenue": total or 0}

# DAILY REVENUE
@router.get("/revenue/daily")
def get_daily_revenue(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    today = datetime.utcnow().date()
    total = db.query(func.sum(Order.total)).filter(
        func.date(Order.created_at) == today,
        Order.payment_status == "paid"
    ).scalar()
    return {"date": str(today), "revenue": total or 0}

# WEEKLY REVENUE
@router.get("/revenue/weekly")
def get_weekly_revenue(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    week_ago = datetime.utcnow() - timedelta(days=7)
    total = db.query(func.sum(Order.total)).filter(
        Order.created_at >= week_ago,
        Order.payment_status == "paid"
    ).scalar()
    return {"period": "last_7_days", "revenue": total or 0}

# TOTAL ORDERS
@router.get("/orders/count")
def get_orders_count(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    total = db.query(func.count(Order.id)).scalar()
    paid = db.query(func.count(Order.id)).filter(Order.payment_status == "paid").scalar()
    pending = db.query(func.count(Order.id)).filter(Order.payment_status == "pending").scalar()
    return {"total_orders": total, "paid": paid, "pending": pending}

# TOP SELLING PRODUCTS
@router.get("/products/top-selling")
def get_top_selling(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    top_products = db.query(
        Product.name,
        func.sum(OrderItem.quantity).label("total_sold")
    ).join(OrderItem, Product.id == OrderItem.product_id)\
     .group_by(Product.name)\
     .order_by(func.sum(OrderItem.quantity).desc())\
     .limit(5).all()
    return [{"product": p.name, "total_sold": p.total_sold} for p in top_products]

# TOTAL CUSTOMERS
@router.get("/customers/count")
def get_customers_count(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    total = db.query(func.count(Customer.id)).scalar()
    return {"total_customers": total}