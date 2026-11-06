# Risk Register & Mitigation Strategy — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** RSK-CITI-001  
**Version:** 1.1.0  
**Status:** Active Risk Tracking  

---

## 1. Risk Matrix Overview

```text
Impact
  High   | [RSK-02: Dirty Ingestion]   [RSK-01: Atlas Free Quota]
  Medium | [RSK-04: Large Browser Dom] [RSK-03: Formula Injection]
  Low    | [RSK-05: Timezone/Date FMT]
         +---------------------------------------------------
           Low                         Medium                 High
                                   Probability
```

---

## 2. Risk Detail & Mitigation Plans

### RSK-01: MongoDB Atlas Free Tier (M0) Storage Quota Exceeded
- **Description:** Atlas M0 offers 512MB storage. Daily line-item POS receipts could exceed 512MB after prolonged usage without rollups.
- **Probability:** Medium | **Impact:** High
- **Mitigation:**
  - Implement rolling aggregations (summarize older daily line items into monthly department rollups).
  - Provide easy export and purge routines for archived fiscal years.
  - Upgrade path to M2/M5 paid shared tier ($9/month) if Citimart store network expands beyond 15 locations.

### RSK-02: Malformed or Corrupt Retail POS Files
- **Description:** Store clerks upload Excel files with missing headers, merged cells, negative quantities, or corrupted dates.
- **Probability:** High | **Impact:** High
- **Mitigation:**
  - 4-step Ingestion Wizard with interactive column preview and fuzzy aliasing.
  - Quarantine mechanism: clean rows are accepted while dirty rows are logged in a downloadable rejection report.

### RSK-03: Spreadsheet Formula Injection (CWE-1236)
- **Description:** Malicious strings starting with `=`, `+`, `-`, `@` executed by Excel on export.
- **Probability:** Low | **Impact:** High
- **Mitigation:**
  - Centralized `sanitize_csv_cell()` prepending `'` to all suspicious strings on export. Validated with automated unit tests.

### RSK-04: DOM Performance on Massive SKU Tables
- **Description:** Tables with thousands of SKUs could cause browser lag or memory bloat.
- **Probability:** Medium | **Impact:** Medium
- **Mitigation:**
  - Pagination and default limit of 50 SKUs with server-side sorting.
  - React 19 optimized rendering with `tabular-nums`.
