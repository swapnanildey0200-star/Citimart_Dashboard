# Project State Memory & Context — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** MEM-CITI-001  
**Version:** 1.1.0  
**Last Verified:** November 6, 2026  
**Status:** Operational & Verified Baseline  

---

## 1. Verified Working Endpoints & Modules

| Module | Route / Subsystem | Verification Method | Status |
| :--- | :--- | :--- | :--- |
| **Executive KPIs** | `GET /api/analytics/kpis` | Pytest & Live API inspection | Verified |
| **4-Question Framework** | `GET /api/analytics/decision-framework`| Response inspection | Verified |
| **Daily Sales Trend** | `GET /api/analytics/sales-trend` | Chart rendering & data verification | Verified |
| **Sales Hierarchy** | `GET /api/analytics/sales-hierarchy` | Multi-level tree grouping verification | Verified |
| **Inventory Ageing** | `GET /api/inventory/ageing-buckets` | 5-tier distribution sum verification | Verified |
| **Stock Velocity** | `GET /api/inventory/velocity-summary` | Cover calculation inspection | Verified |
| **Vendor Concentration**| `GET /api/purchases/vendor-concentration`| Pareto calculation verification | Verified |
| **Alerts Management** | `GET /api/alerts/list` | Acknowledge & resolve status flow | Verified |
| **Spreadsheet Upload** | `POST /api/upload/preview`, `/validate` | Auto-header & alias detection tests | Verified |
| **CSV Export Sanitizer** | `GET /api/export/sales-csv` | Formula neutralization unit tests | Verified |
| **Database Health** | `GET /api/settings/db-health` | Motor & In-memory collection counts | Verified |

---

## 2. Key Codebase Landmarks

- **FastAPI Main App:** `backend/app/main.py` (mounts all 7 routers and CORS).
- **Dual Database Store:** `backend/app/database.py` (`MotorCollectionWrapper` + `ResilientInMemoryCollection`).
- **Core Math & Growth %:** `backend/app/services/analytics_service.py` (`calculate_growth_pct`).
- **Header & File Ingestion:** `backend/app/services/upload_service.py` (`get_auto_mapping`, `validate_stream_data`).
- **CSV Sanitizer:** `backend/app/routers/export.py` (`sanitize_csv_cell`).
- **React Main App:** `frontend/src/App.jsx` (tab state, view switching).
- **Global Filters:** `frontend/src/components/GlobalFilters.jsx`.
- **Indian Number Formatters:** `frontend/src/utils/formatters.js` (`formatCurrency`, `formatNumber`, `formatPercent`).
- **Unit Tests:** `backend/tests/test_analytics_and_validation.py` (passes 100%).

---

## 3. Operational Guarantees
- The app boots and functions immediately even if MongoDB Atlas is offline, thanks to the in-memory fallback.
- No `ZeroDivisionError` is raised when LY is 0.
- All exported CSV cells starting with `=`, `+`, `-`, `@` are safely escaped.
