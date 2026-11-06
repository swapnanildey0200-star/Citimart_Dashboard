# REST API Specification & Contracts — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** API-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  
**Base URL:** `/api` (or `http://127.0.0.1:8000/api`)  
**Interactive Docs:** `http://127.0.0.1:8000/docs` (OpenAPI/Swagger)  

---

## 1. Global Filter Parameters

The majority of analytical endpoints accept uniform query parameters to support dashboard-wide filter synchronization:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `store_id` | `string` | `"all"` | Store identifier (e.g. `"STR001"`) or `"all"` for chain-wide consolidation. |
| `division` | `string` | `"all"` | Merchandise division (e.g. `"Apparel"`, `"Footwear"`). |
| `department` | `string` | `"all"` | Specific merchandise department (e.g. `"Boys Casual"`, `"Women Ethnic"`). |
| `date_range` | `string` | `"30d"` | Preset relative period: `"7d"`, `"30d"`, `"90d"`, `"ty"`, `"custom"`. |
| `start_date` | `string` | `null` | ISO Date `YYYY-MM-DD` when `date_range="custom"`. |
| `end_date` | `string` | `null` | ISO Date `YYYY-MM-DD` when `date_range="custom"`. |

---

## 2. Analytics Router (`/api/analytics`)

### 2.1 Get Executive KPIs
- **Endpoint:** `GET /api/analytics/kpis`
- **Description:** Returns the 10 core management KPIs comparing This Year (TY) to Last Year (LY).
- **Response `200 OK`:**
```json
{
  "total_net_sales": 14258900.0,
  "ly_net_sales": 12890400.0,
  "growth_pct": 10.62,
  "sales_qty": 24150.0,
  "ly_sales_qty": 22400.0,
  "qty_growth_pct": 7.81,
  "asp": 590.43,
  "ly_asp": 575.46,
  "gross_margin_pct": 41.85,
  "stock_qty": 38400.0,
  "stock_value": 10752000.0,
  "stock_cover_days": 47.7,
  "purchase_qty": 18200.0,
  "purchase_value": 5096000.0
}
```

### 2.2 Get 4-Question Decision Framework
- **Endpoint:** `GET /api/analytics/decision-framework`
- **Description:** Synthesizes current retail anomalies into operational questions and corrective actions.
- **Response `200 OK`:**
```json
{
  "what_happened": "Kids Casual Apparel experienced a 21.4% sales decline compared to Last Year.",
  "where_did_it_happen": "Citimart Gariahat Flagship and Citimart New Market.",
  "why_did_it_happen": "Severe stock gap in high-velocity Boys Graphic Printed Cotton Tees (SKU C540112); stock cover dropped below 3 days.",
  "what_action": "Expedite Vendor Purchase Order PO-88210 with Big Sky Fashion and trigger emergency transfer of 250 units from Central Warehouse."
}
```

### 2.3 Get Sales Trend
- **Endpoint:** `GET /api/analytics/sales-trend`
- **Description:** Daily comparison of TY net sales vs LY net sales.
- **Response `200 OK`:**
```json
[
  {"date": "2026-10-08", "ty_sales": 482100.0, "ly_sales": 441200.0},
  {"date": "2026-10-09", "ty_sales": 512400.0, "ly_sales": 478000.0}
]
```

### 2.4 Get Department Contribution
- **Endpoint:** `GET /api/analytics/department-contribution`
- **Description:** Breakdown of sales and margin by merchandise department.
- **Response `200 OK`:**
```json
[
  {"department": "Men Casual", "sales": 4820000.0, "share_pct": 33.8, "margin_pct": 42.1},
  {"department": "Women Ethnic", "sales": 3950000.0, "share_pct": 27.7, "margin_pct": 45.3}
]
```

### 2.5 Get Store Rankings
- **Endpoint:** `GET /api/analytics/store-rankings`
- **Description:** Ranked list of stores by revenue, growth %, and stock cover.
- **Response `200 OK`:**
```json
[
  {
    "store_id": "STR001",
    "name": "Citimart Gariahat",
    "format": "Flagship",
    "sales": 5420000.0,
    "growth_pct": 14.2,
    "stock_cover_days": 41.2
  }
]
```

### 2.6 Get Sales Hierarchy Table
- **Endpoint:** `GET /api/analytics/sales-hierarchy`
- **Description:** Tabular hierarchical breakdown (Division → Section → Department).

### 2.7 Get Product Performance Matrix
- **Endpoint:** `GET /api/analytics/product-performance`
- **Query Params:** `limit=50`, `sort_by="sales"`, `order="desc"`
- **Description:** List of SKUs with revenue, units sold, margin %, and status.

### 2.8 Get Filter Options
- **Endpoint:** `GET /api/analytics/filter-options`
- **Description:** Available stores, divisions, and departments for dropdown population.

---

## 3. Inventory Router (`/api/inventory`)

### 3.1 Get Ageing Buckets
- **Endpoint:** `GET /api/inventory/ageing-buckets`
- **Description:** Stock quantity and valuation split across standard retail ageing buckets.
- **Response `200 OK`:**
```json
[
  {"bucket": "0-30 days", "stock_qty": 14200, "stock_value": 3976000.0, "share_pct": 36.9},
  {"bucket": "31-60 days", "stock_qty": 11500, "stock_value": 3220000.0, "share_pct": 29.9},
  {"bucket": "61-90 days", "stock_qty": 6800, "stock_value": 1904000.0, "share_pct": 17.7},
  {"bucket": "91-180 days", "stock_qty": 4100, "stock_value": 1148000.0, "share_pct": 10.7},
  {"bucket": ">180 days", "stock_qty": 1800, "stock_value": 504000.0, "share_pct": 4.8}
]
```

### 3.2 Get Velocity Summary
- **Endpoint:** `GET /api/inventory/velocity-summary`
- **Description:** Classifies inventory into Fast, Normal, Slow, Non-moving, and Out-of-Stock.

### 3.3 Get Stock List
- **Endpoint:** `GET /api/inventory/stock-list`
- **Description:** Paginated inventory records per SKU and store.

---

## 4. Purchases Router (`/api/purchases`)

### 4.1 Vendor Concentration
- **Endpoint:** `GET /api/purchases/vendor-concentration`
- **Description:** Pareto distribution of top suppliers by purchase volume and share %.

### 4.2 Purchase Intake Ratio
- **Endpoint:** `GET /api/purchases/intake-ratio`
- **Description:** Compares monthly purchase quantity against sales quantity to flag over-intake.

---

## 5. Alerts Router (`/api/alerts`)

### 5.1 List Active Alerts
- **Endpoint:** `GET /api/alerts/list`
- **Query Params:** `status="all"|"new"|"acknowledged"|"resolved"`
- **Response `200 OK`:**
```json
[
  {
    "alert_id": "ALT-2026-0041",
    "rule_id": "FAST_RUNNER_OOS",
    "severity": "critical",
    "title": "Severe Stock Gap: Boys Graphic Printed Cotton Tee",
    "message": "SKU C540112 has stock cover of < 3 days at Citimart Gariahat.",
    "department": "Boys Casual",
    "store_id": "STR001",
    "status": "new",
    "timestamp": "2026-11-06T08:00:00Z"
  }
]
```

### 5.2 Acknowledge Alert
- **Endpoint:** `POST /api/alerts/acknowledge/{alert_id}`
- **Description:** Transitions status from `new` to `acknowledged`.

### 5.3 Resolve Alert
- **Endpoint:** `POST /api/alerts/resolve/{alert_id}`
- **Description:** Marks alert as `resolved`.

### 5.4 Get & Update Thresholds
- **Endpoints:** `GET /api/alerts/thresholds`, `POST /api/alerts/thresholds`
- **Payload:** User-defined sensitivity thresholds (e.g. min gross margin %, max aging days).

---

## 6. Upload & Ingestion Router (`/api/upload`)

### 6.1 Preview Spreadsheet
- **Endpoint:** `POST /api/upload/preview`
- **Payload:** `multipart/form-data` with `file` and `stream_type` (`sales` | `inventory` | `purchases` | `products` | `stores`).
- **Response `200 OK`:**
```json
{
  "detected_headers": ["Bill Date", "Store Code", "Item Code", "Qty", "Net Amt"],
  "suggested_mapping": {
    "date": "Bill Date",
    "store_id": "Store Code",
    "sku": "Item Code",
    "quantity": "Qty",
    "net_sales": "Net Amt"
  },
  "sample_rows": [
    {"Bill Date": "2026-11-04", "Store Code": "STR001", "Item Code": "C540112", "Qty": 3, "Net Amt": 1947}
  ],
  "total_preview_rows": 5
}
```

### 6.2 Validate Mapped Rows
- **Endpoint:** `POST /api/upload/validate`
- **Payload:** JSON with column mappings, file reference token, and stream type.
- **Response `200 OK`:**
```json
{
  "total_rows": 1250,
  "valid_rows": 1248,
  "invalid_rows": 2,
  "errors": [
    {"row": 142, "field": "sku", "reason": "Missing SKU value"},
    {"row": 890, "field": "quantity", "reason": "Negative quantity not allowed"}
  ]
}
```

### 6.3 Commit Batch
- **Endpoint:** `POST /api/upload/commit`
- **Description:** Commits valid rows into MongoDB, updates indexes, and generates job record in `import_jobs`.

### 6.4 Download Templates
- **Endpoint:** `GET /api/upload/templates/{stream}`
- **Description:** Returns clean sample `.csv` template with approved standard column headers.

### 6.5 Ingestion Audit History
- **Endpoint:** `GET /api/upload/history`
- **Description:** Historical log of all import jobs with cleanliness scores.

---

## 7. Export Router (`/api/export`)

All export endpoints return standard CSV files with formula-injection neutralization:

- `GET /api/export/sales-csv`
- `GET /api/export/inventory-csv`
- `GET /api/export/purchases-csv`

---

## 8. Settings Router (`/api/settings`)

### 8.1 Database Health
- **Endpoint:** `GET /api/settings/db-health`
- **Response `200 OK`:**
```json
{
  "status": "connected",
  "database_type": "MongoDB Atlas",
  "collections": {
    "stores": 8,
    "products": 450,
    "vendors": 32,
    "sales_transactions": 24150,
    "inventory_snapshots": 12400,
    "purchase_transactions": 1820,
    "import_jobs": 14,
    "generated_alerts": 6
  }
}
```

### 8.2 Reseed Demo Data
- **Endpoint:** `POST /api/settings/reseed-demo`
- **Description:** Clears and reloads synthetic Citimart retail dataset.

### 8.3 Metrics Glossary
- **Endpoint:** `GET /api/settings/metrics-glossary`
- **Description:** Returns JSON array of retail formulas and mathematical explanations.
