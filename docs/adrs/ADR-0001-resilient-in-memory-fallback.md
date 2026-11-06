# ADR-0001: Resilient Dual-Store Architecture with In-Memory Fallback

**Status:** Accepted  
**Date:** 2026-10-15  
**Author:** Citimart Architecture Team  
**Supercedes:** None  

---

## 1. Context & Problem Statement

Citimart required a cost-effective retail analytics platform deployable on free-tier cloud infrastructure (MongoDB Atlas M0 Free Tier). However, external cloud databases present operational risks during local development, demo sessions, and automated CI test execution:
- IP whitelist restrictions or lack of credentials cause application startup crashes (`ServerSelectionTimeoutError`).
- Transient cloud network disconnects can interrupt retail manager workflows.
- Developers cloning the repository need to run the application immediately without signing up for Atlas or installing MongoDB locally.

## 2. Considered Alternatives

1. **Strict MongoDB Requirement:** Crash on startup if MongoDB Atlas is unreachable. (Rejected: ruins zero-friction onboarding and causes demo failures).
2. **SQLite / DuckDB Embedded Database:** Bundle an embedded relational file database. (Rejected: creates dual schema maintenance overhead between SQL and MongoDB BSON document models).
3. **Resilient In-Memory Collection Store with Parity Wrapper:** Implement an in-memory collection class that matches the exact asynchronous method signatures of Motor (`find`, `find_one`, `insert_many`, `update_one`, `count_documents`) and falls back automatically if the Atlas connection ping fails.

## 3. Decision

We implemented **Alternative 3**:
- When `db_manager.connect()` initializes, it pings Atlas with a 4000ms timeout.
- If successful, it wraps collections in `MotorCollectionWrapper` which automatically converts cursors to lists via `await cursor.to_list(length=None)`.
- If Atlas is offline or credentials are missing, `db_manager` sets `is_connected = False` and routes all collection requests to `ResilientInMemoryCollection`, seeded with realistic Citimart demo data.
- The UI displays an ambient badge indicating current storage status (`MongoDB Atlas` vs `Resilient Fallback Mode`).

## 4. Consequences

### Positive
- Zero-friction developer experience: Clone and run immediately with `python -m uvicorn app.main:app`.
- 100% demo uptime: Dashboard works seamlessly even completely offline.
- Identical asynchronous interface for all analytical services.

### Negative / Tradeoffs
- Writes made in fallback mode do not persist across backend process restarts (by design, intended for demos and testing).

