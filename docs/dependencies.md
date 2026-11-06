# Dependencies & Vendor Governance — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** DEP-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Backend Dependencies (`backend/requirements.txt`)

All backend dependencies are managed through Python pip and isolated in `backend/venv`.

| Package | Minimum Version | License | Category | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **fastapi** | `>=0.115.0` | MIT | Web Framework | Core asynchronous API router, dependency injection, and schema binding. |
| **uvicorn[standard]**| `>=0.30.0` | BSD-3-Clause | ASGI Server | High-performance asynchronous HTTP server hosting FastAPI. |
| **pydantic** | `>=2.9.0` | MIT | Validation | Request parsing, strict schema enforcement, and data serialization. |
| **pydantic-settings**| `>=2.4.0` | MIT | Configuration | Environment variable loading and configuration management. |
| **pymongo** | `>=4.8.0` | Apache 2.0 | Database | Low-level MongoDB protocol driver, BSON encoder, and index specifications. |
| **motor** | `>=3.5.0` | Apache 2.0 | Async Database | AsyncIOMotorClient providing non-blocking MongoDB query execution. |
| **pandas** | `>=2.2.0` | BSD-3-Clause | Analytics | Fast vectorized filtering, grouping, and aggregations for retail metrics. |
| **openpyxl** | `>=3.1.5` | MIT | Spreadsheet Engine | Reading, parsing, and generating Microsoft Excel (`.xlsx`) files. |
| **python-multipart**| `>=0.0.9` | Apache 2.0 | File Ingestion | Streaming parser for multipart file upload requests. |
| **python-dateutil** | `>=2.9.0` | Apache 2.0 | Date Utility | Resilient date parsing across diverse POS date formats. |
| **httpx** | `>=0.27.0` | BSD-3-Clause | HTTP Client | Asynchronous HTTP client for integration testing. |
| **pytest** | `>=8.3.0` | MIT | Testing | Test runner and assertion framework for the test pyramid. |

---

## 2. Frontend Dependencies (`frontend/package.json`)

All frontend libraries are managed via `npm` and bundled using `Vite`.

### Runtime Dependencies
| Package | Version | License | Purpose |
| :--- | :--- | :--- | :--- |
| **react** | `^19.2.8` | MIT | Core UI framework with Concurrent Mode and React 19 hooks. |
| **react-dom** | `^19.2.8` | MIT | DOM rendering target for React components. |
| **tailwindcss** | `^4.3.3` | MIT | Next-generation utility-first styling engine. |
| **@tailwindcss/vite** | `^4.3.3` | MIT | Vite plugin for seamless, lightning-fast Tailwind v4 compilation. |
| **recharts** | `^3.10.1` | MIT | SVG charting library for retail trends and department distributions. |
| **lucide-react** | `^1.52.0` | ISC | Lightweight, scalable icon set for retail metrics and alert badges. |
| **clsx** | `^2.1.1` | MIT | Dynamic classname utility. |
| **tailwind-merge** | `^3.7.0` | MIT | Conflict-free Tailwind class resolution. |

### Development Dependencies
| Package | Version | License | Purpose |
| :--- | :--- | :--- | :--- |
| **vite** | `^8.3.0` | MIT | Rapid development server with HMR and Rollup production bundler. |
| **@vitejs/plugin-react**| `^6.1.1` | MIT | Babel/SWC Fast Refresh integration for React in Vite. |
| **oxlint** | `^1.81.0` | MIT | Ultra-fast Rust-based JavaScript/JSX linter. |
| **@types/react** | `^19.2.18` | MIT | TypeScript type definitions for React. |
| **@types/react-dom** | `^19.2.7` | MIT | TypeScript type definitions for React DOM. |

---

## 3. Dependency Vulnerability & License Compliance

1. **Permissive Licensing:** 100% of production dependencies are licensed under standard permissive open-source licenses (MIT, Apache 2.0, BSD-3-Clause, ISC). No copyleft (GPL / AGPL) libraries are permitted.
2. **Security Audits:**
   - Python: Run `pip audit` or `safety check` during CI pipeline.
   - Node: Run `npm audit` before major version upgrades.
