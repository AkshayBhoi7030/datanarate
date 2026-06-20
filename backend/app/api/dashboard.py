
from fastapi import APIRouter
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.responses import APIResponse
from app.core.logging import logger
from pydantic import BaseModel

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class DashboardStats(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    total_products: int


@router.get("/stats", response_model=APIResponse[DashboardStats])
def get_dashboard_stats():
    engine = create_engine(settings.DATABASE_URL)
    
    total_revenue = 0.0
    total_orders = 0
    total_customers = 0
    total_products = 0
    
    try:
        with engine.connect() as conn:
            # Get total revenue
            result = conn.execute(text("SELECT COALESCE(SUM(total_amount), 0) FROM orders"))
            total_revenue = float(result.scalar() or 0)
            
            # Get total orders
            result = conn.execute(text("SELECT COUNT(*) FROM orders"))
            total_orders = int(result.scalar() or 0)
            
            # Get total customers
            result = conn.execute(text("SELECT COUNT(*) FROM customers"))
            total_customers = int(result.scalar() or 0)
            
            # Get total products
            result = conn.execute(text("SELECT COUNT(*) FROM products"))
            total_products = int(result.scalar() or 0)
            
    except Exception as e:
        logger.error(f"Failed to get dashboard stats: {e}")
    
    return APIResponse(
        data=DashboardStats(
            total_revenue=total_revenue,
            total_orders=total_orders,
            total_customers=total_customers,
            total_products=total_products
        )
    )
