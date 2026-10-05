from fastapi import APIRouter, Body
from typing import Dict, Any, List
from app.services.analytics_service import AnalyticsService
from app.database import db_manager

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.post("/kpi-summary")
async def get_kpi_summary(filters: Dict[str, Any] = Body(default={})):
    return await AnalyticsService.get_kpi_summary(filters)

@router.post("/sales-trend")
async def get_sales_trend(filters: Dict[str, Any] = Body(default={})):
    return await AnalyticsService.get_sales_trend(filters)

@router.post("/department-performance")
async def get_department_performance(filters: Dict[str, Any] = Body(default={})):
    return await AnalyticsService.get_department_performance(filters)

@router.post("/store-performance")
async def get_store_performance(filters: Dict[str, Any] = Body(default={})):
    return await AnalyticsService.get_store_performance(filters)

@router.post("/product-rankings")
async def get_product_rankings(filters: Dict[str, Any] = Body(default={}), limit: int = 10):
    return await AnalyticsService.get_product_rankings(filters, limit=limit)

@router.get("/filter-options")
async def get_filter_options():
    stores_coll = db_manager.get_collection("stores")
    prods_coll = db_manager.get_collection("products")
    vendors_coll = db_manager.get_collection("vendors")

    stores = await stores_coll.find({})
    products = await prods_coll.find({})
    vendors = await vendors_coll.find({})

    divisions = sorted(list(set(p.get("division") for p in products if p.get("division"))))
    sections = sorted(list(set(p.get("section") for p in products if p.get("section"))))
    departments = sorted(list(set(p.get("department") for p in products if p.get("department"))))
    categories = sorted(list(set(p.get("category") for p in products if p.get("category"))))
    brands = sorted(list(set(p.get("brand") for p in products if p.get("brand"))))

    return {
        "stores": [{"id": s["store_id"], "name": s["name"], "region": s.get("region", "")} for s in stores],
        "vendors": [{"id": v["vendor_id"], "name": v["name"]} for v in vendors],
        "divisions": divisions,
        "sections": sections,
        "departments": departments,
        "categories": categories,
        "brands": brands
    }
