from fastapi import APIRouter, Body
from typing import Dict, Any
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/purchases", tags=["purchases"])

@router.post("/summary")
async def get_purchase_summary(filters: Dict[str, Any] = Body(default={})):
    return await AnalyticsService.get_purchase_analytics(filters)
