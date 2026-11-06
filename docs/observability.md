# Observability, Telemetry & Logging — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** OBS-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Logging Standards & Namespaces

The backend standardizes on Python's native `logging` library with dedicated loggers across application subsystems:

| Logger Name | File / Module | Events Logged |
| :--- | :--- | :--- |
| **`citimart.api`** | `app.main` | Server startup, shutdown, route exceptions, request timing. |
| **`citimart.db`** | `app.database` | Atlas connection attempts, ping latencies, in-memory fallback transitions. |
| **`citimart.upload`**| `app.services.upload_service` | File parsing, detected headers, row validation errors, commit totals. |
| **`citimart.analytics`**| `app.services.analytics_service`| Calculation latencies, filter anomalies, safe zero-division triggers. |

### Log Format
```text
2026-11-06 13:21:20 [INFO] citimart.db: Connected to MongoDB Atlas cluster at mongodb+srv://... (latency: 42ms)
2026-11-06 13:21:25 [INFO] citimart.upload: Job JOB-1730901234 completed: 1,248 valid rows, 2 invalid rows committed to sales_transactions.
```

---

## 2. Health Monitoring & Diagnostics

### 2.1 Database & System Health Endpoint
- **Endpoint:** `GET /api/settings/db-health`
- **Output:**
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
If Atlas is disconnected, `"status"` gracefully shifts to `"resilient_fallback"` and reports in-memory counts.

---

## 3. Ingestion Audit Trail (`import_jobs`)

Every file uploaded to the Citimart Dashboard is recorded in the `import_jobs` collection with:
- `job_id`: Unique identifier (`JOB-YYYYMMDD-HHMM`)
- `stream_type`: Target retail dataset (`sales`, `inventory`, `purchases`, etc.)
- `filename`: Original uploaded filename
- `total_rows`, `valid_rows`, `invalid_rows`
- `cleanliness_score`: Percentage of valid rows
- `errors`: Specific row-by-row error details for review in Data Quality View.
