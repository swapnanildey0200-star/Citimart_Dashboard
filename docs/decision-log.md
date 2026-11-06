# Decision Log — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** DEC-CITI-001  
**Version:** 1.1.0  
**Status:** Approved Historical Record  

---

## Historical Decision Record

| Date | ID | Decision Taken | Rationale & Context | Champion |
| :--- | :--- | :--- | :--- | :--- |
| **2026-10-02** | DEC-001 | Selected FastAPI + React 19 architecture | Required sub-second responses for multi-store retail data with zero infrastructure bloat. | Tech Lead |
| **2026-10-08** | DEC-002 | Adopted MongoDB Atlas Free Tier (M0) | Flexible schema accommodates diverse retail register formats; zero monthly cloud cost. | DevOps |
| **2026-10-15** | DEC-003 | Built Resilient In-Memory Dual-Store Fallback | Guarantees zero downtime during demos or network outages; facilitates instant local setup. | Tech Lead |
| **2026-10-22** | DEC-004 | Created The 4-Question Management Box | Retail buyers needed actionable decisions ("What to do"), not just passive charts. | Product Mgr |
| **2026-10-28** | DEC-005 | Enforced CSV formula sanitization (`sanitize_csv_cell`) | Prevented potential CWE-1236 code execution attacks on exported retail spreadsheets. | Security Lead |
| **2026-11-02** | DEC-006 | Handled LY=0 as `"New Entry"` | Eliminated `ZeroDivisionError` on newly launched departments and retail stores. | Lead Engineer |
| **2026-11-06** | DEC-007 | Overhauled full documentation suite in `docs/` | Established complete, authoritative engineering and operational specifications. | Architecture |
