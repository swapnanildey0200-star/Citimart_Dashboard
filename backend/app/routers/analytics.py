from fastapi import APIRouter, Body
from typing import Dict, Any, List
from app.services.analytics_service import AnalyticsService, is_warehouse_location
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

    sales_coll = db_manager.get_collection("sales_transactions")
    inv_coll = db_manager.get_collection("inventory_snapshots")

    def values(field: str, *extra) -> list:
        found = {p.get(field) for p in products if p.get(field)}
        for more in extra:
            found.update(v for v in more if v)
        return sorted(found)

    sales_divs, sales_depts, sales_secs, sales_stores = (
        await sales_coll.distinct("division"), await sales_coll.distinct("department"),
        await sales_coll.distinct("section"), await sales_coll.distinct("store_id"))
    inv_divs, inv_depts, inv_secs = (
        await inv_coll.distinct("division"), await inv_coll.distinct("department"), await inv_coll.distinct("section"))

    divisions = values("division", sales_divs, inv_divs)
    sections = values("section", sales_secs, inv_secs)
    departments = values("department", sales_depts, inv_depts)
    categories = values("category")
    brands = values("brand")

    # Stores: master data plus every shop that actually appears in sales (warehouses are not shops)
    store_options = {s["store_id"]: {"id": s["store_id"], "name": s["name"], "region": s.get("region", "")} for s in stores}
    for sid in sales_stores:
        if sid and sid not in store_options and not is_warehouse_location(sid):
            store_options[sid] = {"id": sid, "name": sid, "region": ""}

    return {
        "stores": sorted(store_options.values(), key=lambda o: o["name"]),
        "vendors": [{"id": v["vendor_id"], "name": v["name"]} for v in vendors],
        "divisions": divisions,
        "sections": sections,
        "departments": departments,
        "categories": categories,
        "brands": brands
    }
