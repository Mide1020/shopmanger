from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.dependencies import admin_only
from app.services import analytics_service

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/revenue")
def get_total_revenue(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return analytics_service.get_total_revenue(db)


@router.get("/revenue/daily")
def get_daily_revenue(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return analytics_service.get_daily_revenue(db)


@router.get("/revenue/weekly")
def get_weekly_revenue(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return analytics_service.get_weekly_revenue(db)


@router.get("/orders/count")
def get_orders_count(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return analytics_service.get_orders_count(db)


@router.get("/products/top-selling")
def get_top_selling(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return analytics_service.get_top_selling(db)


@router.get("/customers/count")
def get_customers_count(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return analytics_service.get_customers_count(db)