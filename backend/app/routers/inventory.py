from fastapi import APIRouter, Body
from typing import Dict, Any
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/inventory", tags=["inventory"])

@router.post("/summary")
async def get_inventory_summary(filters: Dict[str, Any] = Body(default={})):
    return await AnalyticsService.get_inventory_analytics(filters)


@router.post("/stock-gap")
async def get_stock_gap(filters: Dict[str, Any] = Body(default={}), target_cover_days: int = 30):
    return await AnalyticsService.get_stock_gap(filters, target_cover_days=target_cover_days)
