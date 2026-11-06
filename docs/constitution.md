# Engineering Constitution & Authority Hierarchy — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** CST-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Enforced  

---

## 1. Immutable Engineering Principles

The Citimart Dashboard is an enterprise retail analytics platform where computational accuracy, financial integrity, and zero operational downtime are critical. The following principles govern all code, architecture, and deployment decisions:

### Principle 1: Computational Accuracy & Zero-Division Safety
- Retail metrics (Gross Margin %, Growth %, ASP, Stock Cover Days) directly influence purchase orders and stock allocations.
- Mathematical operations must never fail due to zero denominators (e.g. newly introduced departments with LY = 0). Fallbacks must be mathematically sound (`None` rendered as `"New Entry"`).
- Currency rounding must be consistent: intermediate calculations preserve float precision; presentation layers format to 2 decimal places using Indian currency groupings.

### Principle 2: Data Immunity & Defense-in-Depth
- Retail POS and Excel registers are inherently untrusted external inputs. The ingestion engine must never execute or blindly trust raw input.
- Any spreadsheet cell starting with formula symbols (`=`, `+`, `-`, `@`) must be neutralized with a leading apostrophe before export to prevent Dynamic Data Exchange (DDE) or formula-injection exploits.
- Database credentials must remain strictly isolated on the backend server. The client SPA bundle must never contain cloud connection strings or Atlas credentials.

### Principle 3: High Availability via Dual-Store Resilience
- Production and demonstration environments must remain operational even if external cloud connectivity to MongoDB Atlas is interrupted.
- The `ResilientInMemoryCollection` fallback must maintain 100% interface parity with `MotorCollectionWrapper`. No frontend view or backend endpoint may return an unhandled HTTP 500 error due to database disconnects.

### Principle 4: Desktop-First Actionability (The 4 Questions)
- Dashboards exist to drive retail decisions, not merely present decorative visual graphics.
- Features must answer: *What happened?*, *Where did it happen?*, *Why did it happen?*, and *What action should be taken?*.

---

## 2. Authority Hierarchy

When resolving conflicting specifications or questions regarding implementation, the following hierarchy is binding:

1. **Security & Data Safety Baseline:** [`security.md`](security.md), [`constitution.md`](constitution.md)
2. **Approved Product Requirements:** [`prd.md`](prd.md), [`acceptance-criteria.md`](acceptance-criteria.md), and feature contracts in [`features/`](features/)
3. **Architecture & API Contracts:** [`system-architecture.md`](system-architecture.md), [`database.md`](database.md), [`apis.md`](apis.md)
4. **Engineering Standards & Test Gates:** [`code-testing.md`](code-testing.md), [`code-review.md`](code-review.md), [`rules.md`](rules.md)
5. **Operational Records:** [`task.md`](task.md), [`memory.md`](memory.md), [`decision-log.md`](decision-log.md)
