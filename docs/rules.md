# Enforceable Engineering & Agent Rules — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** RUL-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Enforced  

---

## 1. Development & Code Modification Rules

### Rule 1: Test-Driven Change & Regression Safety
- **MUST** run unit tests using `pytest` with `PYTHONPATH=backend` before and after modifying backend logic.
- **MUST NOT** commit code that causes `backend/tests/test_analytics_and_validation.py` to fail.
- **MUST** write regression assertions for any reported defect before implementing the fix.

### Rule 2: Database Operations & Async Discipline
- **MUST** use asynchronous methods (`find`, `find_one`, `insert_one`, `insert_many`, `update_one`, `delete_many`, `count_documents`) provided by `DatabaseManager.get_collection(name)`.
- **MUST NOT** execute synchronous blocking calls inside FastAPI route handlers.
- **MUST** maintain method parity between `MotorCollectionWrapper` and `ResilientInMemoryCollection`.

### Rule 3: Spreadsheet & Input Sanitization
- **MUST** route all CSV exports through `sanitize_csv_cell()` in `backend/app/routers/export.py`.
- **MUST** enforce file size caps (25MB) and mime/extension validation on file uploads in `backend/app/routers/upload.py`.
- **MUST** isolate invalid spreadsheet rows into quarantine logs rather than corrupting database collections or crashing the request.

### Rule 4: Frontend Styling & Number Formatting
- **MUST** format all monetary amounts using `formatCurrency` or `formatCompactCurrency` from `frontend/src/utils/formatters.js`.
- **MUST** apply `tabular-nums` CSS and right-alignment to all numeric table cells.
- **MUST** adhere to the Tailwind CSS v4 design tokens defined in `frontend/src/index.css`.

### Rule 5: Credential Isolation
- **MUST NOT** hardcode database URLs, passwords, or secrets in code or git commits.
- **MUST** load all sensitive settings through Pydantic `BaseSettings` from server-side environment variables or local `.env`.
