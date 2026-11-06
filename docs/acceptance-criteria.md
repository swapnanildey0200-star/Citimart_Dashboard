# Standards for Objective Verification & Acceptance Criteria

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** AC-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Acceptance Criteria by Requirement

### AC-001: Executive Dashboard & The 4-Question Framework (REQ-001)
- **Scenario 1.1: 10 Management KPIs Calculation**
  - **Given** sales and inventory records exist in the database for the selected store and date filter,
  - **When** the Executive Dashboard loads or the filter changes,
  - **Then** the UI must display all 10 KPIs: Total Net Sales, LY Net Sales, Growth %, Sales Qty, ASP, Gross Margin %, Stock Qty, Stock Value, Purchase Qty, Purchase Value.
  - **And** all currency values must use the Indian numbering format (`₹`, Lakhs `L`, Crores `Cr`).

- **Scenario 1.2: Safe Zero-Division in Growth Metric**
  - **Given** a product department or store has positive sales This Year (TY = ₹ 50,000) and zero sales Last Year (LY = ₹ 0),
  - **When** the Growth % KPI is calculated,
  - **Then** the application must NOT throw `ZeroDivisionError`,
  - **And** the KPI badge must display `"New Entry"` instead of `"Infinity%"` or `"NaN"`.

- **Scenario 1.3: 4-Questions Operational Decision Box**
  - **Given** an active retail anomaly (e.g. sales decline or severe stock gap),
  - **When** the Executive Dashboard renders,
  - **Then** the Decision Card must present clear, synthesized text addressing: *1. What happened?*, *2. Where did it happen?*, *3. Why did it happen?*, and *4. What action should be taken?*.

---

### AC-002: Sales Analysis Hierarchy & Protected Export (REQ-002)
- **Scenario 2.1: Division / Section / Department Grouping**
  - **Given** POS sales transactions with varying SKU categories,
  - **When** the user views the Sales Analysis page,
  - **Then** transactions must aggregate cleanly into Division, Section, and Department rows with subtotal calculations.

- **Scenario 2.2: Formula-Injection Neutralization on CSV Export**
  - **Given** a product name containing dangerous formula characters (e.g. `=cmd|'/C calc'!A0` or `-50`),
  - **When** the user clicks "Export to CSV",
  - **Then** the downloaded CSV must prefix the value with a single apostrophe (`'=cmd...`), preventing spreadsheet formula execution.

---

### AC-003: Inventory Ageing & Stock Velocity (REQ-003)
- **Scenario 3.1: 5-Bucket Ageing Distribution**
  - **Given** inventory snapshot records with receipt dates,
  - **When** the Inventory Analysis view is loaded,
  - **Then** stock must be classified into exact buckets: `0–30 days`, `31–60 days`, `61–90 days`, `91–180 days`, and `>180 days`.
  - **And** the share % of each bucket must sum to 100%.

- **Scenario 3.2: Velocity Classification**
  - **Given** an SKU with a calculated stock cover of 8 days,
  - **When** velocity summary is generated,
  - **Then** the SKU must be classified as `"Fast Moving"` (< 15 days cover).

---

### AC-004: Purchase & Vendor Concentration (REQ-004)
- **Scenario 4.1: Vendor Pareto Distribution**
  - **Given** multiple purchase orders across various vendors,
  - **When** Purchase Analysis is opened,
  - **Then** the top suppliers must be ranked by order volume with cumulative concentration % indicated.

---

### AC-005: Alerts Workflow & Threshold Configuration (REQ-007)
- **Scenario 5.1: Severity Badge Assignment**
  - **Given** an SKU where stock cover drops below 3 days on a high-velocity item,
  - **When** the alert engine executes,
  - **Then** an alert with severity `"critical"` and rule `"FAST_RUNNER_OOS"` must be created.

- **Scenario 5.2: Alert Lifecycle State Transition**
  - **Given** an alert in status `"new"`,
  - **When** the user clicks "Acknowledge",
  - **Then** its status must transition to `"acknowledged"`,
  - **When** the user clicks "Resolve",
  - **Then** its status must transition to `"resolved"` and update the active counter in the header.

---

### AC-006: 4-Step Ingestion & Validation Pipeline (REQ-008)
- **Scenario 6.1: Header Auto-Detection & Preamble Skipping**
  - **Given** an Excel file where the first 2 rows contain title text or empty lines,
  - **When** the file is uploaded to `POST /api/upload/preview`,
  - **Then** the engine must correctly detect Row 3 as the real column header row.

- **Scenario 6.2: Fuzzy Column Aliases**
  - **Given** POS register columns titled `"Bill Date"`, `"Store"`, `"Item Code"`, `"Sum of Bill Qty"`,
  - **When** auto-mapping executes,
  - **Then** they must be automatically mapped to `"date"`, `"store_id"`, `"sku"`, and `"quantity"`.

- **Scenario 6.3: Dirty Row Quarantine**
  - **Given** a 100-row file containing 2 rows with missing SKUs or negative quantities,
  - **When** validation executes,
  - **Then** the 98 clean rows must be validated successfully,
  - **And** the 2 dirty rows must be isolated with row numbers and exact rejection reasons displayed in the preview.

---

### AC-007: Resilient Persistence Fallback (REQ-010)
- **Scenario 7.1: MongoDB Atlas Offline Fallback**
  - **Given** the MongoDB Atlas cluster is unreachable or network access is severed,
  - **When** the backend starts up or queries are received,
  - **Then** the application must NOT crash or return HTTP 500,
  - **And** it must automatically serve cached/demo data from `ResilientInMemoryCollection`,
  - **And** the UI header badge must display `"Resilient Fallback Mode"`.
