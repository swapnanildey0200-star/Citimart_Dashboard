# Error Tracker & Incident History — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** ERR-CITI-001  
**Version:** 1.1.0  
**Status:** Active Defect Prevention Baseline  

---

## 1. Resolved Defects & Root Cause Analysis

### INC-001: Motor Async Cursor Iteration Error
- **Symptom:** API calls failed with `TypeError: object AsyncIOMotorCursor can't be used in 'await' expression` or empty document arrays when attempting direct iteration in route handlers.
- **Root Cause:** In the Motor MongoDB driver, `collection.find()` returns an `AsyncIOMotorCursor`, which requires explicit iteration via `async for` or calling `.to_list(length=None)`.
- **Resolution:** Introduced `MotorCollectionWrapper` in `backend/app/database.py`. It wraps every collection returned by `db_manager.get_collection(name)` and automatically calls `await cursor.to_list(length=None)` inside `find()`, ensuring an identical synchronous-like list interface for both MongoDB and the in-memory fallback.
- **Prevention:** Standardized database method signatures across all services; unit and integration tests mandate list-based return validation.

---

### INC-002: ZeroDivisionError on New Category / New Store Growth
- **Symptom:** Backend threw HTTP 500 `ZeroDivisionError: float division by zero` whenever calculating growth % for new merchandise categories or stores that had zero sales in the previous year (LY = 0).
- **Root Cause:** Standard growth formula `((TY - LY) / LY) * 100` did not guard against zero denominator.
- **Resolution:** Created `calculate_growth_pct(ty, ly)` in `backend/app/services/analytics_service.py`:
  ```python
  def calculate_growth_pct(ty: float, ly: float) -> Optional[float]:
      if ly == 0.0:
          return 0.0 if ty == 0.0 else None
      return round(((ty - ly) / ly) * 100.0, 2)
  ```
  On the frontend (`frontend/src/utils/formatters.js`), `null` is formatted cleanly as `"New Entry"`.
- **Prevention:** Added comprehensive unit tests in `backend/tests/test_analytics_and_validation.py` asserting safe division behavior.

---

### INC-003: Interface Discrepancy in Resilient In-Memory Fallback
- **Symptom:** Calling `/api/settings/db-health` failed in in-memory fallback mode because `ResilientInMemoryCollection` lacked the `count_documents()` method.
- **Root Cause:** Initial fallback class only implemented `len(coll.docs)` rather than the full MongoDB async interface.
- **Resolution:** Added `count_documents(query)` and index stubs to `ResilientInMemoryCollection`, ensuring complete 1:1 API parity with `MotorCollectionWrapper`.
- **Prevention:** Verified collection parity in database smoke tests.

---

### INC-004: Spreadsheet Formula Injection Vulnerability (CWE-1236)
- **Symptom:** Exported CSV files could execute unauthorized commands if SKU descriptions contained `=cmd|...` or `-1+1`.
- **Root Cause:** Raw string values were written directly to CSV output without sanitizing leading formula operators.
- **Resolution:** Implemented `sanitize_csv_cell()` in `backend/app/routers/export.py`, prepending `'` to strings starting with `=`, `+`, `-`, `@`.
- **Prevention:** Added unit tests verifying neutralization for all malicious character combinations.

---

### INC-005: Ambiguous POS Date Parsing Across Retailers
- **Symptom:** Ingestion pipeline misread `04/11/2026` as April 11 instead of November 4.
- **Root Cause:** POS cash registers in India typically export dates in `DD/MM/YYYY` format, whereas default pandas parsers assumed US `MM/DD/YYYY`.
- **Resolution:** Configured `python-dateutil` and pandas date parsers in `UploadService` with explicit `dayfirst=True` logic and format sniffing.
- **Prevention:** Added format detection and validation checks to the Ingestion Wizard preview step.
