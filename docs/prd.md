# Product Requirements Document (PRD) — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** PRD-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  
**Product Owner:** Citimart Operations & IT Team  

---

## 1. Problem Statement & Target Audience

### 1.1 The Retail Problem
Retail chain management at Citimart previously relied on fragmented, disparate Excel POS registers, manual vendor purchase summaries, and delayed monthly reports. This caused:
- **Decision Paralysis:** Store managers and department heads spent hours manually collating spreadsheets instead of analyzing trends.
- **Lost Revenue:** Fast-moving products suffered out-of-stock (OOS) conditions while slow-moving styles piled up inventory carrying costs.
- **Lack of Cause-and-Effect Linkage:** Legacy reports showed *what* sales totals were, but failed to connect *where*, *why*, and *what action* management must take.

### 1.2 Target Audience & Personas
1. **Executive Leadership (MD / CEO / COO):** Needs instant high-level visibility into top-line performance, TY vs LY growth %, gross margin, and stock cover across all stores in East India.
2. **Category Buyers / Merchandisers:** Analyze department-level performance, ASP realization, vendor concentration, style/color/size sell-through, and slow-moving stock liquidation.
3. **Store Operations Managers:** Monitor store-specific revenue rankings, stock-to-sales ratios, and daily POS trends.
4. **Data Operations & Inventory Clerks:** Ingest daily/weekly Excel/CSV register dumps, resolve column mappings, correct row errors, and audit data cleanliness.

---

## 2. Core Product Principles: The 4-Question Framework

The entire user experience is built upon an actionable management paradigm that continuously answers four operational questions:
1. **What happened?** (e.g., *Kids department sales declined by 21.4% year-over-year*).
2. **Where did it happen?** (e.g., *Flagship stores Citimart Gariahat and New Market*).
3. **Why did it happen?** (e.g., *Stock gap in high-velocity Boys Graphic Printed Cotton Tees - SKU C540112*).
4. **What action should be taken?** (e.g., *Expedite PO with Big Sky Fashion and trigger emergency transfer of 250 units from Central Warehouse*).

---

## 3. Product Scope & Functional Modules

The application is organized into 10 cohesive, desktop-first analytical modules:

### Module 1: Executive Dashboard (REQ-001)
- Displays **10 Top Management KPIs**: Total Net Sales, Last Year (LY) Sales, Growth %, Total Quantity Sold, Average Selling Price (ASP), Gross Margin %, Stock Quantity, Stock Value, Purchase Quantity, Purchase Value.
- **The 4-Question Decision Card**: AI-grounded operational guidance showing root-cause synthesis and prioritized corrective actions.
- **Interactive Daily Sales Trend**: TY vs LY overlay with hover tooltips and range selectors.
- **Department Contribution Chart**: Visual breakdown of revenue by division and department.
- **Top Stores Leaderboard**: Ranked table comparing store revenue, growth %, and stock cover.
- **Inventory Health Summary**: Quick split of inventory into Fast, Normal, Slow, and Non-moving categories.

### Module 2: Sales Analysis (REQ-002)
- Deep-dive sales performance table grouped by **Division**, **Section**, and **Department**.
- Metrics tracked: TY Sales, LY Sales, Variance %, Quantity Sold, ASP, Gross Margin %, Discount %.
- Comprehensive search, multi-column sorting, and date range filtering.
- Protected CSV export capability.

### Module 3: Inventory & Ageing Analysis (REQ-003)
- Inventory aging distribution across **5 standard retail aging buckets**:
  - `0–30 days` (Fresh Intake)
  - `31–60 days` (Core Active)
  - `61–90 days` (Maturing Stock)
  - `91–180 days` (Slow Moving / Clearance Candidate)
  - `>180 days` (Dead Stock / Immediate Mark-Down)
- **Stock Velocity Classification**:
  - *Fast Moving:* Stock cover < 15 days
  - *Normal:* Stock cover 15–45 days
  - *Slow Moving:* Stock cover 45–90 days
  - *Non-Moving:* Stock cover > 90 days or zero sales in 60 days
  - *Out of Stock:* 0 units on hand with positive historical sales

### Module 4: Purchase & Vendor Analysis (REQ-004)
- Tracking Goods Receipt Notes (GRN) and vendor PO fulfillments.
- **Vendor Concentration Index**: Pareto breakdown of top vendors contributing to 80% of purchases.
- **Intake Ratio**: Comparative analysis of purchase quantity vs sold quantity to identify over-ordering.

### Module 5: Product & SKU Analysis (REQ-005)
- SKU-level drilldown by Style, Color, Size, MRP, Cost Price, and Net Revenue.
- Identification of "Star Performers" (high revenue + high margin) vs "Cash Drains" (high inventory + low sales velocity).

### Module 6: Store Analysis (REQ-006)
- Comparison across store formats: **Flagship**, **Regular**, and **Outlet**.
- Sales per square foot and regional performance benchmarks.

### Module 7: Alerts & Decision Support (REQ-007)
- Automated rule-based engine firing actionable alerts categorized by severity:
  - `Critical`: Severe stockouts on fast runners, margins below minimum threshold (<20%).
  - `Warning`: High ageing stock exceeding 90 days, vendor delivery delays.
  - `Info`: New product category intake milestones.
- Status workflow: `New` → `Acknowledged` → `Resolved`.
- User-configurable threshold modal.

### Module 8: Data Ingestion & Validation Wizard (REQ-008)
- 4-Step Interactive Pipeline:
  1. *File Upload:* Accepts `.xlsx`, `.xls`, `.csv` files up to 25MB for 5 streams (Sales, Inventory, Purchases, Products, Stores).
  2. *Header Detection & Auto-Mapping:* Scans top rows, identifies actual header row even if preceded by metadata, and fuzzy-maps retailer column aliases (e.g., "Bill Date", "Sum of Net Amt").
  3. *Row-by-Row Strict Validation:* Type coercion, range checks, required field checks, duplicate detection against database.
  4. *Commit & Audit:* Atomic batch write with import job summary and downloadable error report.
- Standardized, downloadable CSV templates for all retail streams.

### Module 9: Data Quality Governance (REQ-009)
- Historical log of all import jobs.
- Cleanliness scoring: `(valid_rows / total_rows) * 100`.
- Detailed error breakdown categorizing invalid rows, missing SKUs, negative quantities, and unmapped stores.

### Module 10: System Settings & Metrics Glossary (REQ-010)
- Real-time MongoDB Atlas connection monitor and collection document counters.
- **Zero-Friction Fallback Mode Indicator**: Clear badge indicating whether the app is using Atlas or the Resilient In-Memory store.
- Demo Dataset Reset / Reseed control.
- Interactive Retail Metrics Glossary with formal mathematical definitions.

---

## 4. Non-Functional Requirements

### 4.1 Performance & Latency
- Dashboard KPI queries must compute and render in `< 300ms` for datasets up to 100,000 records.
- Ingestion engine must validate and commit a 10,000-row spreadsheet in `< 3 seconds`.

### 4.2 Security & Data Protection
- **No Direct Frontend DB Access:** All persistence access is mediated through FastAPI.
- **Formula-Injection Neutralization:** Any string starting with `=`, `+`, `-`, or `@` exported to CSV is automatically sanitized with a single quotation prefix `'`.
- **CORS Hardening:** API strictly validates client origin against configured domains.

### 4.3 Resilience & High Availability
- **Resilient Fallback Mode:** In the event of network disruption to MongoDB Atlas, the system seamlessly initializes and serves data from an in-memory repository without crashing or throwing 500 errors.
- **Zero-Division Handling:** When Last Year (LY) value is zero, growth is reported safely as `"New Entry"` or `null` without throwing `ZeroDivisionError` or returning `NaN`.

---

## 5. Requirements Traceability Summary

| Req ID | Title | Module | Priority | Status |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-001** | Executive Dashboard & 4 Questions | Executive Dashboard | P0 | Verified |
| **REQ-002** | Multi-level Sales Hierarchy | Sales Analysis | P0 | Verified |
| **REQ-003** | Inventory Ageing & Velocity | Inventory Analysis | P0 | Verified |
| **REQ-004** | Vendor Concentration & Intake | Purchase Analysis | P1 | Verified |
| **REQ-005** | SKU Matrix & Performance | Product Analysis | P1 | Verified |
| **REQ-006** | Store Format Comparisons | Store Analysis | P1 | Verified |
| **REQ-007** | Rule-Based Alerts Workflow | Alerts View | P1 | Verified |
| **REQ-008** | Ingestion & Mapping Wizard | Upload Pipeline | P0 | Verified |
| **REQ-009** | Ingestion Audit & Quality Log | Data Quality View | P2 | Verified |
| **REQ-010** | Database Health & Seed Utility | Settings View | P0 | Verified |
