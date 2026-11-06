# Pre-Flight Release Checklist — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** CHK-CITI-001  
**Version:** 1.1.0  
**Status:** Mandatory Release Gate  

---

## Pre-Release Verification Protocol

Before merging to `main` or deploying any update to production, every item below must be verified and checked:

### 1. Code Quality & Formatting
- [ ] No extraneous debug statements, mock print statements, or hardcoded passwords left in codebase.
- [ ] Backend code passes clean import checks without circular dependencies.
- [ ] Frontend passes linter without unresolved errors:
  ```powershell
  cd frontend && npm run lint
  ```

### 2. Automated Test Suite
- [ ] Unit tests in `backend/tests/test_analytics_and_validation.py` pass 100%:
  ```powershell
  $env:PYTHONPATH="backend"
  .\backend\venv\Scripts\python.exe -m pytest backend\tests\test_analytics_and_validation.py
  ```
- [ ] Zero-division edge case verified (LY = 0 returns `None` and displays `"New Entry"`).
- [ ] Formula-injection neutralization verified for `=`, `+`, `-`, `@`.
- [ ] Ingestion auto-header and column aliasing tests pass.

### 3. Security & Data Protection
- [ ] `MONGODB_URI` and `SECRET_KEY` are strictly loaded from environment variables and never committed to Git.
- [ ] Frontend bundle verified to contain zero database credentials or internal Atlas URLs.
- [ ] CORS origins in `backend/app/config.py` are properly constrained to the production domain.
- [ ] Exported CSV endpoints sanitize all dynamic spreadsheet formula prefixes.

### 4. Build & Asset Verification
- [ ] Frontend production build compiles with zero errors:
  ```powershell
  cd frontend && npm run build
  ```
- [ ] Output assets in `frontend/dist/` are verified.
- [ ] `frontend/vercel.json` rewrite rules point to the correct production backend URL.

### 5. Database & Resilience Verification
- [ ] MongoDB Atlas compound indexes are verified (`store_id, date`, `sku, date`).
- [ ] Resilient In-Memory fallback mode is tested by launching backend without Atlas and confirming all analytical views load with demo data.
- [ ] Database health endpoint `/api/settings/db-health` returns HTTP 200 and accurate collection counts.
