# Operational Runbook & Incident Response — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** RUN-CITI-001  
**Version:** 1.1.0  
**Status:** Approved Operational Guide  

---

## 1. Routine Developer & Operational Workflows

### 1.1 Starting the Local Environment

#### Backend Server
```powershell
# Navigate to backend directory
cd d:\IT\Citimart_Dashboard\backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start Uvicorn ASGI server with hot reloading
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: `http://127.0.0.1:8000/docs`

#### Frontend Development Server
```powershell
# In a new terminal, navigate to frontend directory
cd d:\IT\Citimart_Dashboard\frontend

# Install packages if not already present
npm install

# Start Vite server
npm run dev -- --host 127.0.0.1 --port 5173
```
Dashboard UI will be live at: `http://127.0.0.1:5173`

---

### 1.2 Re-seeding the Demo Dataset

If demo data becomes fragmented or invalid rows were committed during testing:
1. Open the Dashboard in your browser (`http://127.0.0.1:5173`).
2. Navigate to the **System Settings** tab (last tab in header).
3. Under **Database Health & Maintenance**, click **"Re-seed Demo Data"**.
4. Confirm the prompt. The backend will reset all collections (`stores`, `products`, `vendors`, `sales_transactions`, `inventory_snapshots`, `purchase_transactions`) to the clean, pre-configured Citimart benchmark dataset.

Alternatively, trigger via curl:
```bash
curl -X POST http://127.0.0.1:8000/api/settings/reseed-demo
```

---

## 2. Incident Troubleshooting Procedures

### 2.1 Issue: MongoDB Atlas Connection Dropped / Timeout
- **Symptoms:** Database health indicator in header turns amber; logs show `ServerSelectionTimeoutError`.
- **Automatic Behavior:** The application automatically falls back to `ResilientInMemoryCollection` and continues serving all dashboards with cached demo data. No HTTP 500 errors will be thrown to users.
- **Corrective Steps:**
  1. Check internet connectivity and verify MongoDB Atlas cluster status.
  2. In Atlas dashboard, verify Network Access IP whitelist (`0.0.0.0/0` or the specific backend server IP).
  3. Verify `MONGODB_URI` password encoding if the password contains special characters (e.g. `@`, `#`, `?` must be URL-encoded).
  4. Restart the backend process once connectivity is restored.

---

### 2.2 Issue: Spreadsheet Upload Rejection / Invalid Rows
- **Symptoms:** Upload Wizard displays "Validation Failed" with dirty row count.
- **Diagnosis:**
  1. In the Step 3 preview table, click on the **"Rejection Log"** tab.
  2. Note the flagged row numbers and error descriptions (e.g. `Row 42: Negative quantity not allowed`, `Row 85: Missing SKU`).
- **Remediation:**
  1. Open the source Excel/CSV file.
  2. Correct or remove the highlighted rows.
  3. Download the clean reference template from Step 1 (`/api/upload/templates/{stream}`) to verify column headers.
  4. Re-upload the corrected spreadsheet.
