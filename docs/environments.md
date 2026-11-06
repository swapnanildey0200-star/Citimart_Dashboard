# Environment Configuration Register — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** ENV-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Environments Overview

The Citimart Dashboard supports three distinct operational environments:

| Environment | Purpose | Hosting / Infrastructure | Persistence Mode |
| :--- | :--- | :--- | :--- |
| **Local Development** | Rapid feature prototyping & automated test execution. | Local machine (`127.0.0.1:8000`, `127.0.0.1:5173`). | Local MongoDB instance or automatic In-Memory fallback. |
| **Staging / Preview** | Pre-merge verification, PR reviews, and user acceptance. | Vercel Preview Deployments + Staging Cloud Backend. | MongoDB Atlas Staging cluster (`citimart_staging`). |
| **Production** | Live retail management, daily POS file ingestion. | Vercel Production + Render / Railway Web Service. | MongoDB Atlas Production cluster (`citimart_retail`). |

---

## 2. Environment Variables Matrix

All configuration settings are defined in `backend/app/config.py` using Pydantic `BaseSettings`:

| Variable | Type | Default (Local Dev) | Staging / Production Example | Required? |
| :--- | :--- | :--- | :--- | :--- |
| **`PROJECT_NAME`** | `str` | `"Citimart Retail Analytics Dashboard"` | `"Citimart Retail Dashboard"` | No |
| **`HOST`** | `str` | `"0.0.0.0"` | `"0.0.0.0"` | No |
| **`PORT`** | `int` | `8000` | Assigned by cloud host (e.g. `10000`) | No |
| **`MONGODB_URI`** | `str` | `"mongodb://localhost:27017"` | `"mongodb+srv://user:pass@cluster.mongodb.net/..."` | Yes (in Prod) |
| **`DATABASE_NAME`**| `str` | `"citimart_retail"` | `"citimart_retail"` | No |
| **`CORS_ORIGINS`** | `str` | `"*"` | `"https://citimart.vercel.app"` | Yes (in Prod) |
| **`SECRET_KEY`** | `str` | `"citimart-dev-secret-key-12345"` | Strong random 32-character string | Yes (in Prod) |

---

## 3. Local Development Configuration Template

Create a file named `.env` in `backend/`:

```ini
# Backend Environment Configuration
PROJECT_NAME="Citimart Retail Analytics Dashboard"
HOST=0.0.0.0
PORT=8000

# MongoDB Configuration
# Leave as default to trigger the Resilient In-Memory store if MongoDB is not running locally
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=citimart_retail

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Application Secrets
SECRET_KEY=citimart-super-secret-key-development-mode
```

---

## 4. Frontend Configuration

In local development, Vite connects to the backend running at `http://127.0.0.1:8000`.  
The API client in `frontend/src/services/api.js` automatically routes calls through:
- In Development: direct relative path `/api` configured in Vite dev server proxy or direct URL.
- In Production: `/api` rewritten by `vercel.json` to the production backend URL.
