# GEMINI.md — Agent & Developer Guide for Citimart Dashboard

**Project:** Citimart Retail Analytics & Management Dashboard  
**Framework:** FastAPI (Backend) + React 19 / Vite / Tailwind CSS v4 (Frontend)  
**Database:** MongoDB Atlas (Production) / Resilient In-Memory Dual-Store (Fallback)  
**Primary Reference:** [`docs/INDEX.md`](docs/INDEX.md) | **Authority:** [`docs/constitution.md`](docs/constitution.md) & [`docs/rules.md`](docs/rules.md)

---

## 1. Project Overview & Core Mission

The **Citimart Retail Analytics & Management Dashboard** is a high-performance, cost-effective retail intelligence platform. It ingests, validates, normalizes, and analyzes historical and daily point-of-sale (POS) and stock registers, transforming raw transactional data into executive decision support and granular analytical reports.

### The 4-Question Management Framework
Every view and analytical metric is designed to answer four foundational operational questions:
1. **What happened?** (e.g., *Kids department sales declined by 21.4%*)
2. **Where did it happen?** (e.g., *Citimart Gariahat & New Market flagship stores*)
3. **Why did it happen?** (e.g., *Stock gap in fast-moving Boys Graphic Printed Cotton Tees — SKU C540112*)
4. **What action should be taken?** (e.g., *Expedite vendor PO with Big Sky Fashion and replenish 250 units from Central Warehouse*)

---

## 2. Technology Stack & Key Dependencies

| Layer | Technologies & Libraries |
| :--- | :--- |
| **Backend** | Python 3.11+ / 3.14, FastAPI (`>=0.115.0`), Uvicorn, Pydantic v2 (`>=2.9.0`), Motor / PyMongo, Pandas (`>=2.2.0`), Openpyxl, HTTPX, Pytest |
| **Frontend** | React 19 (`19.2.8`), Vite (`8.3.0`), Tailwind CSS v4 (`@tailwindcss/vite`), Lucide Icons, Recharts (`3.10.1`), Oxlint |
| **Database** | MongoDB Atlas (Free Tier) with compound indexes `(store_id, date)` and `(sku, date)`. Built-in zero-friction in-memory fallback (`ResilientInMemoryCollection`) when Atlas is unreachable |
| **Deployment** | Vercel (Frontend SPA with `/api` rewrite proxy), Render / Railway / Fly.io (Backend container/service) |

---

## 3. Repository Architecture & Layout

```
Citimart_Dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI application entry point & router mounting
│   │   ├── config.py                # Environment configuration via Pydantic BaseSettings
│   │   ├── database.py              # DatabaseManager: Dual-store (Motor + In-Memory Fallback)
│   │   ├── models/
│   │   │   └── schemas.py           # Pydantic models for sales, inventory, POs, alerts, uploads
│   │   ├── routers/
│   │   │   ├── alerts.py            # Alert rules and executive 4-question decision cards
│   │   │   ├── analytics.py         # KPIs, sales trends, department/store aggregations
│   │   │   ├── export.py            # Sanitized CSV export endpoints
│   │   │   ├── health.py            # Health check & DB connection diagnostics
│   │   │   ├── inventory.py         # Inventory aging & stock velocity calculation
│   │   │   ├── purchases.py         # PO tracking, vendor concentration, intake ratios
│   │   │   ├── settings.py          # Metric glossary, system configuration, demo re-seeding
│   │   │   └── upload.py            # Ingestion pipeline: template, validate, commit, history
│   │   └── services/
│   │       ├── analytics_service.py # Core analytical formulas & aggregation logic
│   │       ├── data_generator.py    # Mock/seed retail dataset generator
│   │       └── ingestion_service.py # Header detection, row validation, quarantine logging
│   ├── tests/
│   │   ├── test_analytics_and_validation.py # Unit & regression tests for math & validation
│   │   ├── test_api_endpoints.py            # Integration test script for live endpoints
│   │   └── test_upload_pipeline.py          # End-to-end upload pipeline verification
│   ├── .env                         # Local runtime environment variables
│   ├── .env.example                 # Reference environment template
│   └── requirements.txt             # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ExecutiveDecisionCard.jsx # 4-Question action recommendation box
│   │   │   ├── GlobalFilters.jsx         # Date range, store, and department filter bar
│   │   │   ├── Header.jsx                # Top bar with connection status & quick actions
│   │   │   └── KPICard.jsx               # Metric summary card with TY vs LY variance
│   │   ├── pages/
│   │   │   ├── AlertsView.jsx            # Actionable anomaly and rule-based alerts
│   │   │   ├── DataQualityView.jsx       # Ingestion audit trail & quarantine logs
│   │   │   ├── ExecutiveDashboard.jsx    # Primary 10-KPI executive overview
│   │   │   ├── InventoryAnalysis.jsx     # Ageing buckets & stock cover velocity
│   │   │   ├── ProductAnalysis.jsx       # SKU-level ranking & product performance
│   │   │   ├── PurchaseAnalysis.jsx      # GRN tracking & vendor concentration
│   │   │   ├── SalesAnalysis.jsx         # Departmental hierarchy & sales performance
│   │   │   ├── SettingsView.jsx          # Database status, demo re-seed, formulas
│   │   │   ├── StockGap.jsx              # Stock gap & out-of-stock risk analysis
│   │   │   ├── StoreAnalysis.jsx         # Store rankings & retail format productivity
│   │   │   └── UploadView.jsx            # 4-step ingestion wizard with fuzzy mapping
│   │   ├── services/
│   │   │   └── api.js                   # Axios/fetch API client with proxy handling
│   │   └── utils/
│   │       └── formatters.js            # Indian currency (₹ Lakh/Cr), percent, date formats
│   ├── package.json                 # Frontend scripts & dependencies
│   └── vite.config.js               # Vite config with Tailwind CSS v4 plugin
├── docs/                            # Comprehensive documentation, specs, and constitution
└── Data/                            # Sample Excel/CSV test data registers
```

---

## 4. Development Setup & Essential Commands

### Environment Prerequisites
- Python 3.11+ (Python 3.14 verified)
- Node.js LTS (v20+ or v24 verified) and npm
- Windows PowerShell note: use `npm.cmd` if PowerShell execution policy restricts `.ps1` scripts.

### Backend Commands
```powershell
# Navigate to backend directory
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install / update backend dependencies
pip install -r requirements.txt

# Start backend development server (port 8000)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Run backend unit & validation tests
python -m pytest tests/test_analytics_and_validation.py
```
Backend API documentation (Swagger): `http://127.0.0.1:8000/docs`

### Frontend Commands
```powershell
# Navigate to frontend directory
cd frontend

# Install frontend dependencies
npm.cmd install

# Start Vite dev server (port 5173)
npm.cmd run dev -- --host 127.0.0.1 --port 5173

# Run linter (oxlint)
npm.cmd run lint

# Build production bundle
npm.cmd run build
```
Frontend UI dashboard: `http://127.0.0.1:5173`

---

## 5. Architectural Principles & Enforceable Rules

Agents and developers working on this codebase **MUST** adhere to the standards outlined in [`docs/constitution.md`](docs/constitution.md) and [`docs/rules.md`](docs/rules.md):

### 1. Dual-Store Persistence & Async Parity
- All database operations flow through `DatabaseManager.get_collection(collection_name)`.
- If MongoDB Atlas (`MONGODB_URI`) is not reachable, the system transparently falls back to `ResilientInMemoryCollection`.
- **Rule:** Every collection method used (`find`, `find_one`, `insert_one`, `insert_many`, `update_one`, `delete_many`, `count_documents`) must be **asynchronous** (`await collection.method(...)`).
- **Rule:** Never execute synchronous blocking calls inside FastAPI route handlers.

### 2. Computational Accuracy & Zero-Division Safety
Retail metrics directly influence purchasing and allocation decisions:
- **Growth % Formula:** `((TY - LY) / LY) * 100`. When `LY == 0`, report `None` (rendered on frontend as `"New Entry"`), never throw `ZeroDivisionError` or produce `NaN`.
- **Average Selling Price (ASP):** `Net Sales Amount / Sales Quantity`.
- **Gross Margin %:** `((Net Sales - COGS) / Net Sales) * 100`.
- **Stock Cover (Days):** `Current Stock Quantity / (Period Sales Qty / Period Days)`.
- **Sell-Through Rate (STR %):** `(Units Sold / (Beginning Stock + Received Qty)) * 100`.

### 3. Number & Currency Formatting
- All monetary amounts in the frontend must use `formatCurrency` or `formatCompactCurrency` from `frontend/src/utils/formatters.js` (Indian rupee symbol `₹` with Lakh / Crore grouping).
- All numeric table cells must use the CSS class `tabular-nums` and align to the right (`text-right`).

### 4. Input Sanitization & Anti-Formula Injection
- When generating CSV exports (`backend/app/routers/export.py`), every cell must be sanitized with `sanitize_csv_cell()` to prepend an apostrophe `'` to strings starting with `=`, `+`, `-`, or `@`.
- Ingestion uploads are capped at 25MB and validated against strict Pydantic schemas. Corrupt or unparseable rows must be quarantined to error logs, never crashing the request or corrupting collections.

### 5. Credential & Network Isolation
- Database credentials and connection strings must remain strictly on the backend.
- The client SPA bundle must never receive or expose MongoDB Atlas URLs or secrets.
- Always load server secrets via Pydantic `BaseSettings` (`backend/app/config.py`).

---

## 6. Key Configuration Variables (`.env`)

| Variable | Default / Example | Purpose |
| :--- | :--- | :--- |
| `APP_NAME` | `"Citimart Retail Analytics Dashboard"` | Display name for the application |
| `APP_ENV` | `development` | Environment mode (`development`, `staging`, `production`) |
| `PORT` | `8000` | Backend API port |
| `HOST` | `"0.0.0.0"` | Backend binding host |
| `MONGODB_URI` | `"mongodb://localhost:27017"` | MongoDB connection URI (or fallback to in-memory) |
| `DATABASE_NAME` | `"citimart_retail"` | Primary database name |
| `CORS_ORIGINS` | `"http://localhost:5173,http://127.0.0.1:5173"` | Allowed CORS frontend origins |
| `CURRENCY_CODE` | `"INR"` | Currency representation |
| `NUMBER_FORMAT` | `"lakh_crore"` | Number grouping standard (`lakh_crore` or `standard_thousands`) |
| `MAX_UPLOAD_SIZE_MB` | `200` | Maximum file upload size limit |
| `SECRET_KEY` | `"[secret]"` | Cryptographic key for server-side operations |

---

## 7. Documentation Hierarchy

When resolving requirements or making design decisions, follow this authority hierarchy:
1. **Constitution & Security:** [`docs/constitution.md`](docs/constitution.md), [`docs/security.md`](docs/security.md)
2. **Product Requirements:** [`docs/prd.md`](docs/prd.md), [`docs/acceptance-criteria.md`](docs/acceptance-criteria.md), [`docs/features/`](docs/features/)
3. **Architecture & Database:** [`docs/system-architecture.md`](docs/system-architecture.md), [`docs/database.md`](docs/database.md), [`docs/apis.md`](docs/apis.md)
4. **Engineering Standards & Tests:** [`docs/rules.md`](docs/rules.md), [`docs/code-testing.md`](docs/code-testing.md), [`docs/code-review.md`](docs/code-review.md)
5. **State & Execution:** [`docs/task.md`](docs/task.md), [`docs/memory.md`](docs/memory.md), [`docs/CHANGELOG.md`](docs/CHANGELOG.md)
