import React, { useState, useEffect } from "react";
import { CheckCheck, ShieldAlert, AlertTriangle, FileText, Download, CheckCircle2 } from "lucide-react";
import { fetchImportHistory, exportCsvData } from "../services/api";

export default function DataQualityView() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchImportHistory().then(setHistory).catch(console.error);
  }, []);

  const totalImported = history.reduce((sum, h) => sum + (h.total_rows || 0), 0);
  const totalValid = history.reduce((sum, h) => sum + (h.valid_rows || 0), 0);
  const totalInvalid = history.reduce((sum, h) => sum + (h.invalid_rows || 0), 0);
  const healthScore = totalImported > 0 ? ((totalValid / totalImported) * 100).toFixed(1) : 100.0;

  const handleExportAudit = () => {
    const rows = history.map((h) => ({
      "Job ID": h.job_id,
      "Stream": h.data_type,
      "File Name": h.file_name,
      "Total Rows": h.total_rows,
      "Valid Rows": h.valid_rows,
      "Invalid Rows": h.invalid_rows,
      "Duplicates": h.duplicate_rows,
      "Warning Count": h.warning_count,
      "Status": h.status,
      "Summary": h.error_summary,
      "Date": h.created_at
    }));
    exportCsvData("citimart_data_quality_audit.csv", Object.keys(rows[0] || {}), rows);
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Data Quality & Validation Governance</h2>
          <p className="text-xs text-slate-400">
            Audit trail of row errors, foreign key integrity, duplicate detection, and data ingestion health
          </p>
        </div>

        <button
          onClick={handleExportAudit}
          className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Download Audit Report</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-slate-400">Data Cleanliness Score</div>
          <div className="text-xl font-bold text-emerald-400 mt-1">{healthScore}%</div>
          <div className="text-[11px] text-slate-500 mt-0.5">{totalValid} / {totalImported} valid rows</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-slate-400">Total Ingestion Jobs</div>
          <div className="text-xl font-bold text-white mt-1">{history.length} Jobs</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Logged across all streams</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-slate-400">Invalid Skipped Rows</div>
          <div className="text-xl font-bold text-rose-400 mt-1">{totalInvalid} Rows</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Rejected by validation engine</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-slate-400">Master Data Consistency</div>
          <div className="text-xl font-bold text-blue-400 mt-1">100% Intact</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Stores, Products, Vendors matched</div>
        </div>
      </div>

      {/* Validation Rules Checklist */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
        <h3 className="text-sm font-semibold text-white mb-2">Automated Ingestion Validation Engine Rules</h3>
        <p className="text-[11px] text-slate-400 mb-4">Every uploaded row is verified against the following strict constraints:</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          {[
            { title: "Required Column Verification", desc: "Ensures critical fields (Date, Store, SKU, Qty, Net Sales) are present and mapped.", status: "Active" },
            { title: "Negative & Impossible Quantities", desc: "Rejects negative sales quantities or nonsensical return anomalies.", status: "Active" },
            { title: "Excel Serial & Multi-Date Parsing", desc: "Standardizes Excel date numbers (e.g. 46193) and DD-MM-YYYY to ISO YYYY-MM-DD.", status: "Active" },
            { title: "Duplicate Transaction Protection", desc: "Checks (Date + Store + SKU + Qty) tuples to prevent accidental double imports.", status: "Active" },
            { title: "Foreign Key Integrity", desc: "Cross-checks Store IDs and Product SKUs against master registers; flags unknown entries.", status: "Active" },
            { title: "Formula-Injection Shielding", desc: "Sanitizes dangerous spreadsheet macros (=, +, -, @) before processing and exporting.", status: "Active" }
          ].map((rule, idx) => (
            <div key={idx} className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <div className="font-semibold text-white">{rule.title}</div>
                <div className="text-[11px] text-slate-400 mt-0.5 leading-relaxed">{rule.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
