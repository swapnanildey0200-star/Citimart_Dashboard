import React, { useState, useEffect } from "react";
import { Database, RefreshCw, BookOpen, Server, CheckCircle, ShieldCheck } from "lucide-react";
import { fetchDbStatus, triggerSeedData, fetchMetricGlossary } from "../services/api";

export default function SettingsView({ onDataRefresh }) {
  const [dbStatus, setDbStatus] = useState(null);
  const [glossary, setGlossary] = useState([]);
  const [isSeeding, setIsSeeding] = useState(false);
  const [seedMessage, setSeedMessage] = useState("");

  useEffect(() => {
    loadInfo();
  }, []);

  const loadInfo = async () => {
    try {
      const [status, terms] = await Promise.all([
        fetchDbStatus(),
        fetchMetricGlossary()
      ]);
      setDbStatus(status);
      setGlossary(terms);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSeed = async () => {
    if (!window.confirm("Reload sample Citimart retail dataset? This will refresh all demo collections.")) return;
    setIsSeeding(true);
    setSeedMessage("");
    try {
      const res = await triggerSeedData();
      setSeedMessage(res.message);
      await loadInfo();
      if (onDataRefresh) onDataRefresh();
    } catch (err) {
      setSeedMessage("Failed to seed data: " + err.message);
    } finally {
      setIsSeeding(false);
    }
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
        <h2 className="text-base font-bold text-white tracking-tight">System Settings & Metric Glossary</h2>
        <p className="text-xs text-slate-400">
          Database health, collection metadata, mathematical definitions, and demo dataset controls
        </p>
      </div>

      {/* Database Status & Controls */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Status Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm space-y-3">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
            <Database className="w-4 h-4 text-blue-400" />
            <h3 className="text-sm font-semibold text-white">Database Health</h3>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Connection Mode:</span>
              <span className="font-semibold text-emerald-400 capitalize">
                {dbStatus?.mode || "Checking..."}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-slate-400">Database Name:</span>
              <span className="font-mono text-slate-200">{dbStatus?.database_name || "citimart_retail"}</span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-slate-400">Security Credentials:</span>
              <span className="text-emerald-400 flex items-center gap-1 font-medium">
                <ShieldCheck className="w-3.5 h-3.5" /> Isolated in Backend
              </span>
            </div>
          </div>

          <div className="pt-2 border-t border-slate-800">
            <button
              onClick={handleSeed}
              disabled={isSeeding}
              className="w-full flex items-center justify-center gap-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold py-2 rounded-lg transition-colors cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSeeding ? "animate-spin" : ""}`} />
              <span>{isSeeding ? "Seeding Citimart Data..." : "Reload Citimart Demo Dataset"}</span>
            </button>
            {seedMessage && (
              <p className="text-[11px] text-emerald-400 mt-2 text-center">{seedMessage}</p>
            )}
          </div>
        </div>

        {/* Collection Counts Card */}
        <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-2 mb-3">
            <Server className="w-4 h-4 text-purple-400" />
            <h3 className="text-sm font-semibold text-white">Collection Record Counts</h3>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
            {Object.entries(dbStatus?.counts || {}).map(([coll, count]) => (
              <div key={coll} className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                <div className="text-[11px] text-slate-400 capitalize truncate">
                  {coll.replace("_", " ")}
                </div>
                <div className="text-base font-bold text-white mt-0.5">{count}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Metric Formula Glossary */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-2 mb-3">
          <BookOpen className="w-4 h-4 text-emerald-400" />
          <h3 className="text-sm font-semibold text-white">Retail Metric Definitions & Mathematical Formulas</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          {glossary.map((item, idx) => (
            <div key={idx} className="bg-slate-950 border border-slate-850 p-3 rounded-lg space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white text-xs">{item.metric}</span>
                <span className="text-[10px] bg-slate-850 text-slate-400 px-1.5 py-0.5 rounded font-mono font-semibold">
                  {item.unit}
                </span>
              </div>
              <div className="bg-slate-900/90 font-mono text-[11px] text-blue-300 p-2 rounded border border-slate-800">
                {item.formula}
              </div>
              <p className="text-slate-400 text-[11px] leading-relaxed">
                {item.business_importance}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
