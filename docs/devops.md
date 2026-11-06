# DevOps & Engineering Controls — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** DEV-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Source Control & Branching Strategy

The repository follows a clean GitHub flow:
- **`main` Branch:** Always deployable, representing the current production-ready release.
- **Feature Branches (`feat/<feature-name>`):** Scoped development branches for new analytical views, ingestion enhancements, or bug fixes.
- **Pull Request Gates:** Every PR targeting `main` must pass unit tests and clean frontend build checks.

---

## 2. Continuous Integration Pipeline (GitHub Actions)

A recommended CI workflow (`.github/workflows/ci.yml`) runs on every pull request:

```yaml
name: Citimart CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run Backend Unit Tests
        env:
          PYTHONPATH: backend
        run: |
          pytest backend/tests/test_analytics_and_validation.py

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install Frontend Dependencies
        run: |
          cd frontend
          npm install
      - name: Run Lint & Build
        run: |
          cd frontend
          npm run build
```

---

## 3. Deployment Automation

- **Frontend:** Automatically triggers Vercel edge deployment upon pushing commits to `main`.
- **Backend:** Render / Railway webhook automatically pulls the updated repository and restarts the Uvicorn worker process without dropped connections.
