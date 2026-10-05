import React, { useState, useEffect } from "react";
import {
  UploadCloud,
  FileSpreadsheet,
  CheckCircle,
  AlertTriangle,
  XCircle,
  ArrowRight,
  Download,
  History,
  RefreshCw,
  FileCheck
} from "lucide-react";
import {
  uploadFilePreview,
  validateUploadData,
  commitUploadData,
  fetchImportHistory
} from "../services/api";

const DATA_TYPES = [
  { id: "sales", label: "Daily / Historical Sales" },
  { id: "inventory", label: "Inventory / Stock Snapshot" },
  { id: "purchases", label: "Purchases / GRN Register" },
  { id: "product_master", label: "Product Master" },
  { id: "store_master", label: "Store Master" },
];

export default function UploadView({ onImportComplete }) {
  const [step, setStep] = useState(1); // 1: Select & Upload, 2: Column Mapping, 3: Validation Preview, 4: Success
  const [dataType, setDataType] = useState("sales");
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  // Step 2 State
  const [previewData, setPreviewData] = useState(null);
  const [columnMapping, setColumnMapping] = useState({});
  const [headerRowIdx, setHeaderRowIdx] = useState(1);

  // Step 3 State
  const [validationResult, setValidationResult] = useState(null);

  // Import History
  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const res = await fetchImportHistory();
      setHistory(res);
    } catch (err) {
      console.error(err);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setErrorMsg("");
    }
  };

  const handleStartUpload = async () => {
    if (!selectedFile) {
      setErrorMsg("Please select an Excel (.xlsx/.xls) or CSV file.");
      return;
    }

    setIsProcessing(true);
    setErrorMsg("");
    try {
      const preview = await uploadFilePreview(selectedFile, dataType);
      setPreviewData(preview);
      setColumnMapping(preview.suggested_mapping || {});
      setHeaderRowIdx(preview.detected_header_row || 1);
      setStep(2);
    } catch (err) {
      setErrorMsg(err.message || "Failed to parse file preview.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleValidate = async () => {
    setIsProcessing(true);
    setErrorMsg("");
    try {
      const result = await validateUploadData(selectedFile, dataType, columnMapping, headerRowIdx);
      setValidationResult(result);
      setStep(3);
    } catch (err) {
      setErrorMsg(err.message || "Row validation failed.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCommit = async () => {
    if (!validationResult || !validationResult.valid_records) return;

    setIsProcessing(true);
    setErrorMsg("");
    try {
      await commitUploadData({
        job_id: validationResult.job_id,
        data_type: dataType,
        file_name: selectedFile.name,
        valid_records: validationResult.valid_records,
        stats: {
          file_size_bytes: selectedFile.size,
          total_rows: validationResult.total_rows,
          invalid_rows: validationResult.invalid_rows,
          duplicate_rows: validationResult.duplicate_rows,
          warning_count: validationResult.warning_count
        }
      });
      setStep(4);
      loadHistory();
      if (onImportComplete) onImportComplete();
    } catch (err) {
      setErrorMsg(err.message || "Failed to commit import.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleResetFlow = () => {
    setStep(1);
    setSelectedFile(null);
    setPreviewData(null);
    setValidationResult(null);
    setErrorMsg("");
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Data Upload & Validation Pipeline</h2>
          <p className="text-xs text-slate-400">
            Ingest POS Sales, Stock Snapshots, Purchases, or Masters with intelligent column mapping and strict row validation
          </p>
        </div>

        {/* Step Indicator */}
        <div className="flex items-center gap-2 text-xs">
          {[
            { num: 1, label: "Select File" },
            { num: 2, label: "Column Mapping" },
            { num: 3, label: "Validate & Review" },
            { num: 4, label: "Imported" }
          ].map((s) => (
            <div
              key={s.num}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md border ${
                step === s.num
                  ? "bg-blue-600 text-white border-blue-500 font-bold"
                  : step > s.num
                  ? "bg-emerald-950/40 text-emerald-300 border-emerald-800"
                  : "bg-slate-950 text-slate-500 border-slate-800"
              }`}
            >
              <span>{s.num}.</span>
              <span>{s.label}</span>
            </div>
          ))}
        </div>
      </div>

      {errorMsg && (
        <div className="bg-rose-950/40 border border-rose-800/80 rounded-xl p-3 text-xs text-rose-300 flex items-center gap-2">
          <XCircle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* STEP 1: Select Data Type & Upload File */}
      {step === 1 && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                1. Select Data Stream Type
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {DATA_TYPES.map((dt) => (
                  <button
                    key={dt.id}
                    onClick={() => setDataType(dt.id)}
                    className={`p-2.5 rounded-lg border text-left text-xs font-medium transition-all cursor-pointer ${
                      dataType === dt.id
                        ? "bg-blue-600/20 border-blue-500 text-white ring-1 ring-blue-500"
                        : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                    }`}
                  >
                    {dt.label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                2. Choose Excel (.xlsx) or CSV (.csv) File
              </label>
              <div className="border-2 border-dashed border-slate-800 hover:border-blue-500 rounded-xl p-8 text-center bg-slate-950/50 transition-colors">
                <FileSpreadsheet className="w-10 h-10 mx-auto text-blue-400 mb-2 opacity-80" />
                <p className="text-xs font-semibold text-white mb-1">
                  {selectedFile ? selectedFile.name : "Drag & drop file here, or click to browse"}
                </p>
                <p className="text-[11px] text-slate-400 mb-3">
                  Supports multi-sheet POS exports, daily sale registers, stock gap sheets
                </p>
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload-input"
                />
                <label
                  htmlFor="file-upload-input"
                  className="inline-flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold px-4 py-2 rounded-lg cursor-pointer border border-slate-700 transition-colors"
                >
                  <UploadCloud className="w-3.5 h-3.5" />
                  <span>Select File</span>
                </label>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={handleStartUpload}
                disabled={!selectedFile || isProcessing}
                className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-5 py-2.5 rounded-lg transition-colors cursor-pointer disabled:opacity-50"
              >
                <span>{isProcessing ? "Reading Headers..." : "Continue to Column Mapping"}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Sample Templates Download Box */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-col justify-between">
            <div>
              <h3 className="text-sm font-semibold text-white mb-1">Sample CSV Templates</h3>
              <p className="text-[11px] text-slate-400 mb-3">
                Download pre-formatted templates with realistic Citimart headers and sample rows:
              </p>

              <div className="space-y-2 text-xs">
                {DATA_TYPES.map((dt) => (
                  <a
                    key={dt.id}
                    href={`/api/upload/template/${dt.id}`}
                    download
                    className="flex items-center justify-between p-2 rounded-lg bg-slate-950 hover:bg-slate-850 border border-slate-800 text-slate-300 hover:text-white transition-colors"
                  >
                    <span>{dt.label} Template</span>
                    <Download className="w-3.5 h-3.5 text-blue-400" />
                  </a>
                ))}
              </div>
            </div>

            <div className="mt-4 p-2.5 rounded-lg bg-blue-950/30 border border-blue-900/40 text-[11px] text-blue-300">
              <strong>Tip:</strong> You don't need exact column names. The next step allows you to map any uploaded column headers to Citimart fields.
            </div>
          </div>
        </div>
      )}

      {/* STEP 2: Column Mapping Wizard */}
      {step === 2 && previewData && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 className="text-sm font-bold text-white">Map File Columns to Citimart Schema</h3>
              <p className="text-xs text-slate-400">
                File: <strong>{previewData.filename}</strong> (Detected Header Row: #{headerRowIdx})
              </p>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setStep(1)}
                className="text-xs text-slate-400 hover:text-white px-3 py-1.5 rounded-lg bg-slate-800 cursor-pointer"
              >
                Back
              </button>
              <button
                onClick={handleValidate}
                disabled={isProcessing}
                className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-1.5 rounded-lg cursor-pointer"
              >
                <span>{isProcessing ? "Validating..." : "Validate Data Rows"}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Mapping Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {Object.keys(columnMapping).map((targetField) => {
              const isRequired = (previewData.required_fields || []).includes(targetField);
              return (
                <div key={targetField} className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-slate-200 capitalize">
                      {targetField.replace("_", " ")}
                    </span>
                    {isRequired && (
                      <span className="text-[10px] text-rose-400 font-bold uppercase tracking-wider">Required</span>
                    )}
                  </div>
                  <select
                    value={columnMapping[targetField] || ""}
                    onChange={(e) =>
                      setColumnMapping({
                        ...columnMapping,
                        [targetField]: e.target.value || null
                      })
                    }
                    className="w-full bg-slate-900 border border-slate-700 text-slate-200 px-2 py-1.5 rounded focus:outline-none focus:border-blue-500 cursor-pointer"
                  >
                    <option value="">-- Do Not Map --</option>
                    {previewData.headers.map((h, i) => (
                      <option key={`${h}_${i}`} value={h}>
                        {h}
                      </option>
                    ))}
                  </select>
                </div>
              );
            })}
          </div>

          {/* Raw File Preview Table */}
          <div className="pt-2">
            <h4 className="text-xs font-semibold text-slate-300 mb-2">First 5 Sample Rows from File</h4>
            <div className="overflow-x-auto border border-slate-800 rounded-lg">
              <table className="w-full text-left text-[11px]">
                <thead className="bg-slate-950 text-slate-400">
                  <tr>
                    {previewData.headers.map((h, i) => (
                      <th key={i} className="p-2 border-b border-slate-800 whitespace-nowrap">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 bg-slate-900/60">
                  {previewData.preview_rows.slice(0, 5).map((row, ri) => (
                    <tr key={ri}>
                      {row.map((val, ci) => (
                        <td key={ci} className="p-2 text-slate-300 whitespace-nowrap">
                          {String(val || "")}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* STEP 3: Validation Review & Error Report */}
      {step === 3 && validationResult && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 className="text-sm font-bold text-white">Validation Summary</h3>
              <p className="text-xs text-slate-400">
                File: <strong>{validationResult.file_name}</strong> | Total Rows: <strong>{validationResult.total_rows}</strong>
              </p>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setStep(2)}
                className="text-xs text-slate-400 hover:text-white px-3 py-1.5 rounded-lg bg-slate-800 cursor-pointer"
              >
                Back to Mapping
              </button>

              <button
                onClick={handleCommit}
                disabled={validationResult.valid_rows === 0 || isProcessing}
                className="flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold px-4 py-1.5 rounded-lg cursor-pointer disabled:opacity-50"
              >
                <span>{isProcessing ? "Importing..." : `Import ${validationResult.valid_rows} Valid Rows`}</span>
                <CheckCircle className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Validation Metrics Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <div className="text-slate-400">Total File Rows</div>
              <div className="text-lg font-bold text-white mt-0.5">{validationResult.total_rows}</div>
            </div>

            <div className="bg-emerald-950/30 p-3 rounded-lg border border-emerald-800/40">
              <div className="text-emerald-400">Valid Rows to Import</div>
              <div className="text-lg font-bold text-emerald-300 mt-0.5">{validationResult.valid_rows}</div>
            </div>

            <div className="bg-rose-950/30 p-3 rounded-lg border border-rose-800/40">
              <div className="text-rose-400">Invalid / Skipped Rows</div>
              <div className="text-lg font-bold text-rose-300 mt-0.5">{validationResult.invalid_rows}</div>
            </div>

            <div className="bg-amber-950/30 p-3 rounded-lg border border-amber-800/40">
              <div className="text-amber-400">Duplicates Detected</div>
              <div className="text-lg font-bold text-amber-300 mt-0.5">{validationResult.duplicate_rows}</div>
            </div>
          </div>

          {/* Error Details List if any */}
          {validationResult.errors && validationResult.errors.length > 0 && (
            <div className="bg-slate-950 p-3 rounded-lg border border-rose-900/50">
              <div className="flex items-center gap-1.5 text-xs font-bold text-rose-400 mb-2">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>Validation Errors Detected ({validationResult.errors.length}):</span>
              </div>
              <div className="max-h-48 overflow-y-auto space-y-1.5 text-[11px]">
                {validationResult.errors.map((err, i) => (
                  <div key={i} className="flex items-start gap-2 text-slate-300 border-b border-slate-850 pb-1">
                    <span className="font-mono text-rose-400 font-bold shrink-0">Row #{err.row_number}:</span>
                    <span>{err.reason}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* STEP 4: Success Message */}
      {step === 4 && (
        <div className="bg-slate-900 border border-emerald-800 rounded-xl p-8 text-center shadow-sm space-y-3">
          <CheckCircle className="w-12 h-12 mx-auto text-emerald-400" />
          <h3 className="text-base font-bold text-white">Data Ingested Successfully!</h3>
          <p className="text-xs text-slate-300 max-w-md mx-auto">
            All valid records have been normalized, indexed, and stored. Your management dashboard and analytical reports have been recalculated.
          </p>
          <div className="pt-2">
            <button
              onClick={handleResetFlow}
              className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg cursor-pointer"
            >
              Upload Another File
            </button>
          </div>
        </div>
      )}

      {/* Historical Upload Log */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <History className="w-4 h-4 text-slate-400" />
            <h3 className="text-sm font-semibold text-white">Recent Import History & Audit Log</h3>
          </div>
          <button
            onClick={loadHistory}
            className="text-xs text-slate-400 hover:text-white flex items-center gap-1 cursor-pointer"
          >
            <RefreshCw className="w-3 h-3" /> Refresh Log
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                <th className="pb-2">Job ID</th>
                <th className="pb-2">Stream</th>
                <th className="pb-2">File Name</th>
                <th className="pb-2 text-right">Total Rows</th>
                <th className="pb-2 text-right">Valid Rows</th>
                <th className="pb-2 text-right">Invalid Rows</th>
                <th className="pb-2">Status</th>
                <th className="pb-2 text-right">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {history.map((job) => (
                <tr key={job.job_id} className="hover:bg-slate-850/50 transition-colors">
                  <td className="py-2.5 font-mono text-blue-400 font-medium">{job.job_id}</td>
                  <td className="py-2.5 text-slate-300 uppercase text-[11px] font-semibold">{job.data_type}</td>
                  <td className="py-2.5 text-white font-medium">{job.file_name}</td>
                  <td className="py-2.5 text-right text-slate-300">{job.total_rows}</td>
                  <td className="py-2.5 text-right font-bold text-emerald-400">{job.valid_rows}</td>
                  <td className="py-2.5 text-right text-rose-400">{job.invalid_rows}</td>
                  <td className="py-2.5">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-emerald-950/40 text-emerald-400 border border-emerald-800">
                      {job.status}
                    </span>
                  </td>
                  <td className="py-2.5 text-right text-slate-400 text-[11px]">
                    {job.created_at ? job.created_at.slice(0, 16).replace("T", " ") : ""}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
