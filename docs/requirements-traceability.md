# Requirements Traceability Matrix — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** RTM-CITI-001  
**Version:** 1.1.0  
**Status:** Complete Traceability Baseline  

---

## 1. Traceability Matrix

| Req ID | Requirement Description | UI Component | Backend Router & Endpoint | Test Verification |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-001** | Executive Dashboard (10 KPIs & 4 Questions) | `ExecutiveDashboard.jsx`, `KPICard.jsx`, `ExecutiveDecisionCard.jsx` | `app/routers/analytics.py` (`/api/analytics/kpis`, `/decision-framework`) | `test_analytics_and_validation.py` |
| **REQ-002** | Multi-level Sales Hierarchy & CSV Export | `SalesAnalysis.jsx` | `app/routers/analytics.py` (`/sales-hierarchy`), `export.py` (`/sales-csv`) | `test_sanitize_csv_cell` |
| **REQ-003** | Inventory Ageing (5 Buckets) & Velocity | `InventoryAnalysis.jsx` | `app/routers/inventory.py` (`/ageing-buckets`, `/velocity-summary`) | Integration assertions |
| **REQ-004** | Vendor Concentration & Intake Ratio | `PurchaseAnalysis.jsx` | `app/routers/purchases.py` (`/vendor-concentration`, `/intake-ratio`) | Integration assertions |
| **REQ-005** | Product & SKU Matrix (Stars vs Drains) | `ProductAnalysis.jsx` | `app/routers/analytics.py` (`/product-performance`) | Integration assertions |
| **REQ-006** | Store Format Comparisons & Rankings | `StoreAnalysis.jsx` | `app/routers/analytics.py` (`/store-rankings`) | Integration assertions |
| **REQ-007** | Rule-Based Alerts & Lifecycle Workflow | `AlertsView.jsx` | `app/routers/alerts.py` (`/list`, `/acknowledge`, `/resolve`) | Status transition tests |
| **REQ-008** | 4-Step Ingestion & Validation Wizard | `UploadView.jsx` | `app/routers/upload.py` (`/preview`, `/validate`, `/commit`) | `test_auto_mapping_aliases` |
| **REQ-009** | Ingestion Audit History & Cleanliness | `DataQualityView.jsx` | `app/routers/upload.py` (`/history`) | Collection query tests |
| **REQ-010** | System Settings, DB Health & Demo Reseed | `SettingsView.jsx`, `Header.jsx` | `app/routers/settings.py` (`/db-health`, `/reseed-demo`, `/metrics-glossary`) | DatabaseManager health test |
