from fastapi import APIRouter
from app.database import db_manager
from app.services.seed_data import seed_database

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/db-status")
async def get_db_status():
    return await db_manager.get_status()

@router.post("/seed-data")
async def trigger_seed(force: bool = True):
    await seed_database(force=force)
    return {"success": True, "message": "Demo retail database seeded successfully with Citimart dataset."}

@router.get("/metric-glossary")
async def get_metric_glossary():
    return [
        {
            "metric": "Total Sales (TY Net Sales)",
            "formula": "Sum of Net Sales Amount for This Year (TY) within the active filter window.",
            "business_importance": "Core revenue indicator after deducting item-level discounts and promotions.",
            "unit": "Currency (₹)"
        },
        {
            "metric": "LY Sales & Growth %",
            "formula": "Growth % = ((TY - LY) / LY) * 100. If LY = 0, classified as 'New Entry' instead of invalid divide-by-zero.",
            "business_importance": "Key performance benchmark comparing current performance against the corresponding prior year period.",
            "unit": "Percentage (%)"
        },
        {
            "metric": "Average Selling Price (ASP)",
            "formula": "ASP = Net Sales Amount / Sales Quantity",
            "business_importance": "Measures price realization per unit sold across stores and departments.",
            "unit": "₹ / unit"
        },
        {
            "metric": "Gross Margin & Margin %",
            "formula": "Gross Margin = Net Sales - COGS; Margin % = (Gross Margin / Net Sales) * 100",
            "business_importance": "Reflects retail product profitability before store overhead and operating expenses.",
            "unit": "Percentage (%)"
        },
        {
            "metric": "Stock Cover (Days of Inventory)",
            "formula": "Daily Run Rate = Sales Qty / Days in Period; Stock Cover = Current Stock Qty / Daily Run Rate",
            "business_importance": "Forecasts how many days current inventory will last based on recent velocity. Under 7 days = stockout risk; Over 90 days = overstocked.",
            "unit": "Days"
        },
        {
            "metric": "Sell-Through Percentage (STR %)",
            "formula": "STR % = (Units Sold / (Beginning Stock Qty + Received Qty)) * 100",
            "business_importance": "Measures how effectively newly received merchandise is converted into customer sales.",
            "unit": "Percentage (%)"
        },
        {
            "metric": "Stock Aging Buckets",
            "formula": "Age = Current Date - Receipt / First Invoice Date. Grouped into: 0-30d, 31-60d, 61-90d, 91-180d, >180d.",
            "business_importance": "Identifies slow-moving dead inventory tying up working capital before it becomes obsolete.",
            "unit": "Buckets"
        }
    ]
