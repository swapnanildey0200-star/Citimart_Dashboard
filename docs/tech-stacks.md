# Technology Stack Specification — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** TECH-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Complete Technology Inventory

### 1.1 Frontend Architecture
| Layer / Library | Version | Decision Rationale & Purpose |
| :--- | :--- | :--- |
| **React** | `19.2.8` | Component-based UI with React 19 concurrent features, transition hooks, and lightning-fast virtual DOM diffing. |
| **Vite** | `8.3.0` | Next-generation frontend build tool providing instant hot module replacement (HMR) and optimized rollup production bundles. |
| **Tailwind CSS** | `4.3.3` | Modern utility-first CSS framework (v4 engine) enabling rapid styling, consistent design tokens, and minimal final CSS footprint. |
| **Recharts** | `3.10.1` | Declarative, SVG-based charting library built specifically for React, offering smooth animations, custom tooltips, and responsive layout. |
| **Lucide React** | `1.52.0` | Clean, consistent, lightweight SVG icon system for retail indicators, severity badges, and status icons. |
| **Clsx & Tailwind-Merge**| `2.1.1` / `3.7.0` | Utility functions for conditionally merging Tailwind classes without CSS specificity collisions. |

### 1.2 Backend Architecture
| Layer / Library | Version | Decision Rationale & Purpose |
| :--- | :--- | :--- |
| **Python** | `3.14` (also 3.11+) | High-performance modern Python runtime with superior typing capabilities and native async event loop speedups. |
| **FastAPI** | `>=0.115.0` | Asynchronous high-performance web framework based on Starlette and Pydantic with automated OpenAPI/Swagger documentation generation. |
| **Uvicorn** | `>=0.30.0` | Lightning-fast ASGI server implementation for hosting FastAPI applications. |
| **Pydantic & Settings** | `>=2.9.0` | Schema validation, type enforcement, and declarative `.env` configuration management. |
| **Motor (Async MongoDB)**| `>=3.5.0` | Non-blocking, asynchronous Python driver for MongoDB Atlas operations. |
| **PyMongo** | `>=4.8.0` | Core synchronous MongoDB utility library used for BSON serialization and index declarations. |
| **Pandas** | `>=2.2.0` | Vectorized analytical operations, date range filtering, and tabular aggregation calculations. |
| **Openpyxl** | `>=3.1.5` | Native parsing and generation of Microsoft Excel (`.xlsx`) files for store POS uploads. |
| **Python-Multipart** | `>=0.0.9` | High-efficiency streaming multipart form-data parser for handling large spreadsheet uploads. |
| **Pytest** | `>=8.3.0` | Robust testing framework for unit, integration, and pipeline validation tests. |

### 1.3 Database & Hosting
| Component | Provider / Solution | Configuration | Rationale |
| :--- | :--- | :--- | :--- |
| **Primary Database** | MongoDB Atlas | M0 Sandbox (Free Tier, 512MB storage) | Document-oriented flexibility for evolving retail schemas, compound indexing, zero infrastructure costs. |
| **Resilient Fallback** | In-Memory Collection Store | Custom Python Async Collection Store | Ensures zero downtime during demos or network connection loss to cloud database. |
| **Frontend Hosting** | Vercel | Edge CDN with `/api` proxy rewrite | Free global CDN distribution, automatic GitHub deployments, and sub-100ms asset delivery. |
| **Backend Hosting** | Render / Railway / Fly.io | Standard Container / Free Tier Web Service | Simple deployment via Docker or native Python runtime with automatic HTTPS certificates. |

---

## 2. Selection Rationale & Tradeoffs

### Why FastAPI over Django / Flask?
- **Speed & Async I/O:** FastAPI's native async event loop enables handling concurrent analytical dashboard queries without thread-blocking.
- **Automatic Validation & Documentation:** Pydantic models automatically validate incoming requests and generate interactive OpenAPI documentation at `/docs`.
- **Zero Overhead:** Unlike Django, FastAPI avoids ORM bloat, making it ideal for vectorized analytics with Pandas and document stores like MongoDB.

### Why React 19 + Tailwind v4 over Heavy UI Libraries (MUI/AntD)?
- **Bundle Size:** Tailwind v4 generates only the exact CSS utility classes used, reducing total stylesheet size to under 20KB.
- **Customization Flexibility:** Citimart requires compact, high-information-density desktop tables and KPI cards tailored for retail managers; off-the-shelf component libraries introduce unwanted padding and rigid styling abstractions.

### Why Dual-Store Architecture (Atlas + Resilient In-Memory)?
- **No Developer Friction:** New developers or reviewers can clone the repo and run both frontend and backend instantly without needing to configure Atlas credentials or install a local MongoDB service.
- **High Availability in Demonstrations:** If external internet connectivity is unstable, the backend gracefully falls back to the in-memory store and continues serving all analytical views without throwing HTTP 500 errors.

---

## 3. Platform & Runtime Compatibility Matrix

| Runtime / Tool | Minimum Version | Tested & Verified Version | Supported Platforms |
| :--- | :--- | :--- | :--- |
| **Python** | 3.11.0 | 3.14.7 | Windows 10/11, macOS, Linux (Ubuntu/Debian) |
| **Node.js** | 20.0.0 LTS | 24.1.0 LTS | Windows, macOS, Linux |
| **npm** | 10.0.0 | 11.0.0 | Windows, macOS, Linux |
| **Modern Browser** | Chrome 110+, Edge 110+, Firefox 115+, Safari 16+ | Chrome 130+, Edge 130+ | Desktop (Optimized for 1080p, 1440p, 4K) |
