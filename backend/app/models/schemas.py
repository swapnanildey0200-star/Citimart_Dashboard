from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime, date

class StoreModel(BaseModel):
    store_id: str
    name: str
    region: str = "East"
    store_type: str = "Flagship"  # Flagship, Regular, Outlet
    opening_date: Optional[str] = None
    status: str = "Active"

class ProductModel(BaseModel):
    sku: str
    name: str
    division: str
    section: str
    department: str
    category: str = "General"
    brand: str = "Raphaaa"
    style: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    vendor_id: Optional[str] = None
    mrp: float = 0.0
    cost_price: Optional[float] = None

class VendorModel(BaseModel):
    vendor_id: str
    name: str
    category: Optional[str] = None
    contact: Optional[str] = None
    lead_time_days: int = 14

class SalesTransactionModel(BaseModel):
    transaction_id: str
    date: str  # YYYY-MM-DD
    store_id: str
    sku: str
    quantity: float
    selling_price: float
    gross_sales: float
    discount: float = 0.0
    net_sales: float
    rsp: Optional[float] = None
    cogs: Optional[float] = None
    is_void: bool = False
    period_type: str = "TY"  # TY = This Year, LY = Last Year
    import_job_id: Optional[str] = None

class InventorySnapshotModel(BaseModel):
    snapshot_date: str  # YYYY-MM-DD
    store_id: str
    sku: str
    stock_qty: float
    unit_cost: float = 0.0
    stock_value: float = 0.0
    last_sale_date: Optional[str] = None
    receipt_date: Optional[str] = None
    age_days: int = 0
    import_job_id: Optional[str] = None

class PurchaseTransactionModel(BaseModel):
    po_id: str
    date: str  # YYYY-MM-DD
    store_id: str
    vendor_id: str
    sku: str
    quantity: float
    unit_cost: float
    purchase_value: float
    grc_no: Optional[str] = None
    import_job_id: Optional[str] = None

class ImportJobModel(BaseModel):
    job_id: str
    data_type: str  # sales, inventory, purchases, product_master, store_master
    file_name: str
    file_size_bytes: int = 0
    total_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0
    duplicate_rows: int = 0
    warning_count: int = 0
    status: str = "completed"  # pending, processing, completed, failed
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    error_summary: Optional[str] = None

class ImportErrorModel(BaseModel):
    job_id: str
    row_number: int
    field: str
    value: Optional[str] = None
    reason: str
    severity: str = "error"  # error, warning

class AlertRuleModel(BaseModel):
    rule_id: str
    name: str
    metric: str
    condition: str  # drop_percentage, threshold_min, threshold_max, aging_days
    threshold: float
    severity: str = "warning"  # critical, warning, info
    is_active: bool = True

class AlertModel(BaseModel):
    alert_id: str
    rule_id: str
    severity: str  # critical, warning, info
    title: str
    what_happened: str
    where_happened: str
    why_happened: str
    action_recommended: str
    metric_value: float
    threshold_value: float
    status: str = "new"  # new, acknowledged, resolved
    target_page: str = "sales"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class GlobalFilterParams(BaseModel):
    date_preset: Optional[str] = "ytd"  # today, yesterday, wtd, mtd, ytd, custom
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    compare_with: Optional[str] = "LY"  # LY = Last Year, PREV = Previous Period
    stores: Optional[List[str]] = None
    divisions: Optional[List[str]] = None
    sections: Optional[List[str]] = None
    departments: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    brands: Optional[List[str]] = None
    vendors: Optional[List[str]] = None

class KPICardsSummary(BaseModel):
    total_sales: float = 0.0
    ly_sales: float = 0.0
    growth_pct: Optional[float] = None
    growth_val: float = 0.0
    sales_qty: float = 0.0
    ly_sales_qty: float = 0.0
    sales_qty_growth_pct: Optional[float] = None
    asp: float = 0.0
    ly_asp: float = 0.0
    gross_margin: float = 0.0
    gross_margin_pct: float = 0.0
    stock_qty: float = 0.0
    stock_value: float = 0.0
    stock_cover_days: Optional[float] = None
    sell_through_pct: Optional[float] = None
    purchase_qty: float = 0.0
    purchase_value: float = 0.0
