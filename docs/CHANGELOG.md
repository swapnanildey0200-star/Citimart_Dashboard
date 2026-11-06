# Product & Feature Changelog — Citimart Retail Dashboard

All notable changes to the **Citimart Retail Analytics & Management Dashboard** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-11-06

### Added
- **The 4-Question Management Framework:** Automated root-cause synthesis card on the Executive Dashboard answering *What happened?*, *Where did it happen?*, *Why did it happen?*, and *What action should be taken?*.
- **Dual-Store Resilience Engine:** Introduced `MotorCollectionWrapper` and `ResilientInMemoryCollection` in `backend/app/database.py`, allowing the entire dashboard to operate with zero friction and zero crashes when MongoDB Atlas is offline or unconfigured.
- **Spreadsheet Formula-Injection Protection (CWE-1236):** Added `sanitize_csv_cell()` to sanitize dangerous formula prefixes (`=`, `+`, `-`, `@`) in CSV exports.
- **Auto-Header & Column Aliasing Engine:** Enhanced `UploadService` to automatically detect header rows preceded by metadata and fuzzy-map diverse retailer column names (e.g. `"Bill Date"` -> `"date"`, `"Sum of Net Amt"` -> `"net_sales"`).
- **Comprehensive Documentation Suite:** Fully populated `docs/` with complete PRD, system architecture, database specifications, REST API contracts, UI design system, operational runbooks, and Architectural Decision Records (ADRs).

### Changed
- **Safe Zero-Division Growth %:** Refactored `calculate_growth_pct` in `analytics_service.py` to return `None` when Last Year (LY) is 0, rendered in the UI as `"New Entry"` instead of raising `ZeroDivisionError` or showing `NaN`.
- **Indian Numbering System Formatters:** Enhanced `frontend/src/utils/formatters.js` with Lakhs (`L`) and Crores (`Cr`) compact notation for KPI cards.
- **Tailwind v4 Upgrades:** Streamlined frontend CSS with Tailwind CSS v4 and dynamic theme tokens.

### Fixed
- Fixed Motor MongoDB driver async cursor iteration by standardizing on `cursor.to_list(length=None)`.
- Fixed missing `count_documents()` in in-memory fallback collection to ensure 1:1 API parity.
- Fixed date parsing ambiguity for retail POS registers using `DD/MM/YYYY` date formats.

---

## [1.0.0] - 2026-10-05

### Added
- Initial project release of Citimart Retail Analytics Dashboard.
- FastAPI backend with 7 routers (`analytics`, `inventory`, `purchases`, `alerts`, `upload`, `export`, `settings`).
- React 19 desktop-first dashboard with 10 analytical views.
- MongoDB Atlas schema design for stores, products, vendors, sales transactions, inventory snapshots, and purchase orders.
- Basic CSV/Excel upload capability.
