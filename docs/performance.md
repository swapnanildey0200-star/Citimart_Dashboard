# Performance Constraints & Optimization Standards — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** PERF-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Performance SLAs & Latency Budgets

| Operation | Target Budget | Maximum Acceptable | Measured Baseline |
| :--- | :--- | :--- | :--- |
| **Executive KPIs API (`/api/analytics/kpis`)** | `< 150ms` | `< 300ms` | `~45ms` (in-memory) / `~120ms` (Atlas) |
| **Daily Sales Trend (`/api/analytics/sales-trend`)** | `< 200ms` | `< 350ms` | `~60ms` |
| **Sales Hierarchy Tree (`/api/analytics/sales-hierarchy`)** | `< 250ms` | `< 400ms` | `~85ms` |
| **Spreadsheet Upload Preview (10,000 rows)** | `< 1.5s` | `< 3.0s` | `~1.2s` |
| **Spreadsheet Batch Commit (10,000 rows)** | `< 2.0s` | `< 4.0s` | `~1.8s` |
| **Frontend Initial Page Load (FCP)** | `< 0.8s` | `< 1.5s` | `~0.6s` via Vercel CDN |

---

## 2. Backend & Database Optimization

### 2.1 Compound Indexing Strategy
To avoid full collection scans when computing retail KPIs, all queries leverage compound indexes:
- `(store_id, date)`: Restricts sales transactions to the requested store and time window in a single B-tree traversal.
- `(sku, date)`: Quickly isolates daily units sold for stock cover calculations.
- `(period_type, date)`: Bypasses unnecessary scans when segregating This Year (TY) vs Last Year (LY) records.

### 2.2 Vectorized Pandas Aggregations
Rather than performing sequential loops over raw dictionaries, `AnalyticsService` converts fetched BSON lists into Pandas DataFrames. This enables:
- Vectorized column math for Gross Sales, Discount, Net Sales, and Margin.
- Native C-optimized `.groupby(["division", "department"])` aggregations.
- Instant quantile filtering and variance percentage calculations.

---

## 3. Frontend Optimization

1. **Lightweight Bundle:** Using Tailwind CSS v4 and Tree-shakeable Lucide icons keeps total JavaScript bundle size `< 180KB` (gzipped).
2. **Debounced Filter Dispatch:** Changing store or date filters debounces network requests by 250ms to prevent rapid-fire redundant API requests.
3. **Tabular Numerals Rendering:** Using `tabular-nums` CSS prevents layout shifts and repaints when numbers change during real-time filtering.
