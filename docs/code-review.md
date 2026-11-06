# Code Review & PR Standards — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** REV-CITI-001  
**Version:** 1.1.0  
**Status:** Approved Review Standard  

---

## 1. Pull Request Acceptance Criteria

Every Pull Request submitted to the Citimart Dashboard repository must adhere to the following checklist before merge approval:

### 1.1 Architecture & Resilience
- [ ] No direct synchronous blocking calls in FastAPI route handlers; use async methods.
- [ ] Database interactions must route through `DatabaseManager.get_collection(name)`.
- [ ] Any new mathematical metric must handle zero denominators safely (no raw division by `0` or `0.0`).

### 1.2 Security & Data Protection
- [ ] No database credentials, passwords, or connection strings in code or frontend assets.
- [ ] Any new CSV or Excel export endpoint must apply `sanitize_csv_cell()` to prevent formula injection.
- [ ] Uploaded files must validate extension, mime type, and file size limits.

### 1.3 UI & Presentation
- [ ] All currency values must format via `frontend/src/utils/formatters.js` with `₹` and Indian grouping.
- [ ] Table numbers must use `tabular-nums` CSS and right-aligned layout.
- [ ] Tailwind styling must adhere to the slate/indigo design tokens.

### 1.4 Automated Tests
- [ ] New functionality must be accompanied by unit tests in `backend/tests/`.
- [ ] All unit tests pass with 100% success rate.
