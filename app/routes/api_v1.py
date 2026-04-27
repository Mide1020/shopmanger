from fastapi import APIRouter
from . import (
    auth, products, inventory, customers, 
    orders, analytics, customer_routes, 
    product_images, invoice
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(inventory.router)
api_router.include_router(customers.router)
api_router.include_router(orders.router)
api_router.include_router(analytics.router)
api_router.include_router(customer_routes.router)
api_router.include_router(product_images.router)
api_router.include_router(invoice.router)
