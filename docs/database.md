# Database Architecture & Persistence Contract — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** DB-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Persistence Overview

The Citimart Dashboard utilizes a flexible, document-oriented persistence architecture backed by **MongoDB Atlas** (Free Tier M0) and a high-availability **Resilient In-Memory Collection Store**.

All database queries are executed asynchronously through `DatabaseManager` in `backend/app/database.py`, ensuring non-blocking operations across all analytical routers.

```text
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Application Layer                   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                     get_db() -> db_manager
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
       is_connected == True            is_connected == False
                 │                               │
                 ▼                               ▼
      MotorCollectionWrapper         ResilientInMemoryCollection
                 │                               │
                 ▼                               ▼
      MongoDB Atlas Database         In-Memory Python Structures
     ("citimart_retail" M0)          (Pre-seeded with demo data)
```

---

## 2. Collections & Data Schemas

### 2.1 Collection: `stores`
Stores the master list of retail locations, operational regions, and store formats.

```json
{
  "_id": "ObjectId or string",
  "store_id": "STR001",
  "name": "Citimart Gariahat Flagship",
  "region": "East",
  "store_type": "Flagship",
  "opening_date": "2018-04-12",
  "status": "Active"
}
```

- **Indexed Fields:** `store_id` (Unique, Ascending)
- **Supported Formats:** `Flagship`, `Regular`, `Outlet`

---

### 2.2 Collection: `products`
Master catalog of retail SKUs categorized according to Citimart's department hierarchy.

```json
{
  "_id": "ObjectId or string",
  "sku": "C540112",
  "name": "Boys Graphic Printed Cotton Tee",
  "division": "Apparel",
  "section": "Kids Wear",
  "department": "Boys Casual",
  "category": "T-Shirts",
  "brand": "Raphaaa",
  "style": "Graphic Crew",
  "color": "Royal Blue",
  "size": "M",
  "vendor_id": "VND001",
  "mrp": 699.00,
  "cost_price": 280.00
}
```

- **Indexed Fields:** `sku` (Unique, Ascending), `division`, `department`

---

### 2.3 Collection: `vendors`
Approved suppliers, manufacturers, and lead-time tracking.

```json
{
  "_id": "ObjectId or string",
  "vendor_id": "VND001",
  "name": "Big Sky Fashion Pvt Ltd",
  "category": "Apparel Manufacturing",
  "contact": "+91 98301 23456",
  "lead_time_days": 14
}
```

- **Indexed Fields:** `vendor_id` (Unique, Ascending)

---

### 2.4 Collection: `sales_transactions`
Line-item retail POS receipts including pricing, discount, and period classification.

```json
{
  "_id": "ObjectId or string",
  "transaction_id": "TXN-2026-009124",
  "date": "2026-11-04",
  "store_id": "STR001",
  "sku": "C540112",
  "quantity": 3.0,
  "selling_price": 649.00,
  "gross_sales": 2097.00,
  "discount": 150.00,
  "net_sales": 1947.00,
  "rsp": 699.00,
  "cogs": 840.00,
  "is_void": false,
  "period_type": "TY",
  "import_job_id": "JOB-1730901234"
}
```

- **Compound Indexes:**
  - `(store_id, date)`: Accelerates store-level daily sales filtering.
  - `(sku, date)`: Accelerates SKU sales velocity computations.
  - `(period_type, date)`: Accelerates TY vs LY comparative queries.

---

### 2.5 Collection: `inventory_snapshots`
Daily or periodic stock counts, valuation, and ageing metrics per SKU per store.

```json
{
  "_id": "ObjectId or string",
  "snapshot_date": "2026-11-05",
  "store_id": "STR001",
  "sku": "C540112",
  "stock_qty": 42.0,
  "unit_cost": 280.00,
  "stock_value": 11760.00,
  "last_sale_date": "2026-11-04",
  "receipt_date": "2026-09-15",
  "age_days": 51,
  "import_job_id": "JOB-1730901234"
}
```

- **Compound Indexes:**
  - `(store_id, sku)`: Unique snapshot locator.
  - `(age_days)`: Accelerates 5-tier ageing bucket aggregation.

---

### 2.6 Collection: `purchase_transactions`
Goods Receive Register (GRN) and vendor PO fulfillments.

```json
{
  "_id": "ObjectId or string",
  "po_id": "PO-88210",
  "date": "2026-10-20",
  "store_id": "STR001",
  "vendor_id": "VND001",
  "sku": "C540112",
  "quantity": 100.0,
  "unit_cost": 280.00,
  "total_cost": 28000.00,
  "status": "Received"
}
```

---

### 2.7 Collection: `import_jobs`
Audit trail of every spreadsheet uploaded via the Ingestion Pipeline.

```json
{
  "_id": "ObjectId or string",
  "job_id": "JOB-20261106-1145",
  "stream_type": "sales",
  "filename": "Gariahat_POS_Register_Nov2026.xlsx",
  "timestamp": "2026-11-06T11:45:00Z",
  "total_rows": 1250,
  "valid_rows": 1248,
  "invalid_rows": 2,
  "status": "Completed",
  "cleanliness_score": 99.84,
  "errors": [
    {"row": 142, "reason": "Missing SKU code"},
    {"row": 890, "reason": "Negative quantity value: -5"}
  ]
}
```

---

### 2.8 Collection: `generated_alerts`
Active operational alerts generated by the rule engine.

```json
{
  "_id": "ObjectId or string",
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
```

---

## 3. Resilient In-Memory Collection Wrapper

When MongoDB Atlas is unreachable or unconfigured, `ResilientInMemoryCollection` handles operations with parity:

| Method | Behavior in Atlas (`MotorCollectionWrapper`) | Behavior in Fallback Store |
| :--- | :--- | :--- |
| `find(query, sort, limit)` | Executes query on Atlas, converts cursor to `List[Dict]` | Filters in-memory list matching key-value pairs |
| `find_one(query)` | Single document lookup on Atlas | Returns first matching dictionary in memory |
| `insert_one(doc)` | Single document insert on Atlas | Appends dictionary with generated UUID string `_id` |
| `insert_many(docs)` | Batch document insert on Atlas | Appends list of dictionaries |
| `update_one(query, update)`| Updates matched document on Atlas | Modifies fields matching `$set` in memory |
| `delete_many(query)` | Deletes matching documents on Atlas | Filters out matched records |
| `count_documents(query)` | Returns document count on Atlas | Returns count of matching dictionaries in memory |

---

## 4. Compound Indexing Plan

Run the following commands in MongoDB shell to verify production indexes:

```javascript
db.sales_transactions.createIndex({ store_id: 1, date: 1 });
db.sales_transactions.createIndex({ sku: 1, date: 1 });
db.sales_transactions.createIndex({ period_type: 1, date: 1 });
db.inventory_snapshots.createIndex({ store_id: 1, sku: 1 });
db.inventory_snapshots.createIndex({ age_days: 1 });
db.products.createIndex({ sku: 1 }, { unique: true });
db.stores.createIndex({ store_id: 1 }, { unique: true });
```
