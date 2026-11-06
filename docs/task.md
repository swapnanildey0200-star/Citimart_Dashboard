# Task Register & Sprint Tracking — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** TSK-CITI-001  
**Version:** 1.1.0  
**Status:** Active Sprint & Maintenance Register  

---

## 1. Implementation Status Overview

| Workstream | Total Tasks | Completed | In Progress | Backlog |
| :--- | :--- | :--- | :--- | :--- |
| **Ingestion Pipeline & Dual Persistence** | 6 | 6 | 0 | 0 |
| **Analytical Routers & Business Logic** | 8 | 8 | 0 | 0 |
| **Frontend Views & UI Components** | 10 | 10 | 0 | 0 |
| **Security & Data Sanitization** | 4 | 4 | 0 | 0 |
| **Documentation & System Standards** | 10 | 10 | 0 | 0 |

---

## 2. Completed Milestones & Tasks

### Epic 1: Ingestion Pipeline & Persistence Resilience
- [x] **TSK-101:** Implement `UploadService` with auto-header detection and preamble row skipping.
- [x] **TSK-102:** Implement fuzzy column aliasing (e.g., mapping `"Bill Date"` to `"date"`).
- [x] **TSK-103:** Implement row-by-row data type validation and quarantine for invalid rows.
- [x] **TSK-104:** Create `MotorCollectionWrapper` to unify async list conversion across MongoDB operations.
- [x] **TSK-105:** Implement `ResilientInMemoryCollection` fallback store for zero-downtime operation without MongoDB.
- [x] **TSK-106:** Generate pre-seeded synthetic retail dataset for Citimart (stores, products, vendors, sales, stock).

### Epic 2: Analytics & Decision Support
- [x] **TSK-201:** Implement Executive KPIs calculation (`/api/analytics/kpis`) with 10 management metrics.
- [x] **TSK-202:** Implement the **4-Question Management Framework** decision synthesis card.
- [x] **TSK-203:** Implement safe zero-division handling for TY vs LY growth calculations (`calculate_growth_pct`).
- [x] **TSK-204:** Implement 5-bucket inventory ageing distribution (`0-30d`, `31-60d`, `61-90d`, `91-180d`, `>180d`).
- [x] **TSK-205:** Implement stock velocity classification (Fast, Normal, Slow, Non-moving, Out of Stock).
- [x] **TSK-206:** Build Vendor Concentration (Pareto 80/20) and Purchase Intake ratio endpoints.
- [x] **TSK-207:** Build rule-based alert generation with status workflow (`new` → `acknowledged` → `resolved`).
- [x] **TSK-208:** Implement spreadsheet formula-injection neutralization (`sanitize_csv_cell`).

### Epic 3: Desktop-First React Frontend
- [x] **TSK-301:** Build Global Filter Bar (`GlobalFilters.jsx`) with multi-store and date preset selectors.
- [x] **TSK-302:** Build Executive Dashboard (`ExecutiveDashboard.jsx`) with 10 KPI cards and trend charts.
- [x] **TSK-303:** Build Sales Analysis table (`SalesAnalysis.jsx`) with multi-column sorting and CSV export.
- [x] **TSK-304:** Build Inventory & Ageing view (`InventoryAnalysis.jsx`).
- [x] **TSK-305:** Build Purchase & Vendor view (`PurchaseAnalysis.jsx`).
- [x] **TSK-306:** Build Product & SKU view (`ProductAnalysis.jsx`).
- [x] **TSK-307:** Build Store Analysis view (`StoreAnalysis.jsx`).
- [x] **TSK-308:** Build Alerts & Notification view (`AlertsView.jsx`) with threshold edit modal.
- [x] **TSK-309:** Build 4-Step Ingestion Wizard (`UploadView.jsx`).
- [x] **TSK-310:** Build System Settings & Health Monitor (`SettingsView.jsx`).

### Epic 4: Comprehensive Documentation
- [x] **TSK-401:** Overhaul `docs/` folder with complete system specifications, contracts, and architecture guides.
- [x] **TSK-402:** Update `docs/INDEX.md`, `docs/prd.md`, `docs/system-architecture.md`, and `docs/apis.md`.
- [x] **TSK-403:** Author Architectural Decision Records (`adrs/`) for fallback persistence and the 4-Question framework.
