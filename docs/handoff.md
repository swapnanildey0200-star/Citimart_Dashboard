# Project Handoff & Maintenance Guide — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** HND-CITI-001  
**Version:** 1.1.0  
**Status:** Approved Handoff Baseline  

---

## 1. Quick Onboarding Checklist for New Engineers

Welcome to the **Citimart Retail Analytics & Management Dashboard** project! Here is your quickstart guide:

1. **Clone & Explore:**
   - Review [`INDEX.md`](INDEX.md) for document authority and architecture links.
   - Review [`prd.md`](prd.md) for business rules and the 4-Question Framework.
   - Review [`system-architecture.md`](system-architecture.md) for data flows and the dual-store persistence model.

2. **Run Locally:**
   - Backend:
     ```powershell
     cd backend
     .\venv\Scripts\Activate.ps1
     python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
     ```
   - Frontend:
     ```powershell
     cd frontend
     npm install
     npm run dev -- --host 127.0.0.1 --port 5173
     ```
   - Open `http://127.0.0.1:5173`. If MongoDB Atlas is not configured, the app runs automatically in **Resilient Fallback Mode** with complete synthetic retail data.

3. **Verify Tests:**
   ```powershell
   $env:PYTHONPATH="backend"
   .\backend\venv\Scripts\python.exe -m pytest backend\tests\test_analytics_and_validation.py
   ```

---

## 2. Key Maintenance Contacts & Credentials

- **Repository:** Citimart_Dashboard on Git / GitHub
- **Production Frontend:** Vercel Dashboard (linked to `main` branch)
- **Production Backend:** Render / Railway Web Service
- **Database:** MongoDB Atlas cluster (`citimart_retail`)
- **Key Secrets:** Stored securely in Cloud Provider Environment Variables (`MONGODB_URI`, `SECRET_KEY`, `CORS_ORIGINS`). Never commit `.env` to Git.
