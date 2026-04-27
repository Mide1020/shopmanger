from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.customer import Customer
from app.logger import get_logger
from datetime import datetime, timedelta, timezone

logger = get_logger(__name__)


def get_total_revenue(db: Session) -> dict:
    total = db.query(func.sum(Order.total)).filter(
        Order.payment_status == "paid",
        Order.deleted_at.is_(None)
    ).scalar()
    return {"total_revenue": total or 0}


def get_daily_revenue(db: Session) -> dict:
    today = datetime.now(timezone.utc).date()
    total = db.query(func.sum(Order.total)).filter(
        func.date(Order.created_at) == today,
        Order.payment_status == "paid",
        Order.deleted_at.is_(None)
    ).scalar()
    return {"date": str(today), "revenue": total or 0}


def get_weekly_revenue(db: Session) -> dict:
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    total = db.query(func.sum(Order.total)).filter(
        Order.created_at >= week_ago,
        Order.payment_status == "paid",
        Order.deleted_at.is_(None)
    ).scalar()
    return {"period": "last_7_days", "revenue": total or 0}


def get_orders_count(db: Session) -> dict:
    base = db.query(func.count(Order.id)).filter(Order.deleted_at.is_(None))
    total = base.scalar()
    paid = base.filter(Order.payment_status == "paid").scalar()
    pending = base.filter(Order.payment_status == "pending").scalar()
    return {"total_orders": total, "paid": paid, "pending": pending}


def get_top_selling(db: Session, limit: int = 5) -> list:
    top_products = (
        db.query(
            Product.name,
            func.sum(OrderItem.quantity).label("total_sold")
        )
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.deleted_at.is_(None))
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )
    return [{"product": p.name, "total_sold": p.total_sold} for p in top_products]


def get_customers_count(db: Session) -> dict:
    total = db.query(func.count(Customer.id)).filter(Customer.deleted_at.is_(None)).scalar()
    return {"total_customers": total}
