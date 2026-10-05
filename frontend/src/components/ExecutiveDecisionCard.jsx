import React from "react";
import { AlertCircle, HelpCircle, MapPin, Compass, CheckCircle2 } from "lucide-react";

export default function ExecutiveDecisionCard({ decisionData, onNavigateAlerts }) {
  if (!decisionData) return null;

  const { what, where, why, action, critical_count } = decisionData;

  return (
    <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-900/50 rounded-xl p-4 shadow-lg mb-4">
      <div className="flex items-center justify-between gap-3 mb-3 border-b border-indigo-900/40 pb-2.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-indigo-600/20 border border-indigo-500/30 rounded-lg text-indigo-400">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white tracking-wide flex items-center gap-2">
              Retail Decision Support Engine
              {critical_count > 0 && (
                <span className="text-[10px] bg-rose-500/20 text-rose-300 border border-rose-500/40 px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">
                  {critical_count} Critical Action{critical_count > 1 ? "s" : ""} Required
                </span>
              )}
            </h3>
            <p className="text-[11px] text-slate-400">
              Automated root-cause diagnostics answering the 4 core management questions
            </p>
          </div>
        </div>

        {onNavigateAlerts && (
          <button
            onClick={onNavigateAlerts}
            className="text-xs font-medium text-indigo-300 hover:text-white bg-indigo-950/60 hover:bg-indigo-900/60 border border-indigo-800/80 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
          >
            View All Rules & Alerts →
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
        {/* 1. What Happened */}
        <div className="bg-slate-900/80 border border-slate-800/80 rounded-lg p-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-1.5 text-amber-400 font-semibold mb-1">
              <AlertCircle className="w-3.5 h-3.5" />
              <span>1. What Happened?</span>
            </div>
            <p className="text-slate-200 leading-relaxed text-[11.5px]">{what}</p>
          </div>
        </div>

        {/* 2. Where Did It Happen */}
        <div className="bg-slate-900/80 border border-slate-800/80 rounded-lg p-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-1.5 text-blue-400 font-semibold mb-1">
              <MapPin className="w-3.5 h-3.5" />
              <span>2. Where?</span>
            </div>
            <p className="text-slate-200 leading-relaxed text-[11.5px]">{where}</p>
          </div>
        </div>

        {/* 3. Why Did It Happen */}
        <div className="bg-slate-900/80 border border-slate-800/80 rounded-lg p-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-1.5 text-purple-400 font-semibold mb-1">
              <HelpCircle className="w-3.5 h-3.5" />
              <span>3. Why Did It Happen?</span>
            </div>
            <p className="text-slate-200 leading-relaxed text-[11.5px]">{why}</p>
          </div>
        </div>

        {/* 4. What Action to Take */}
        <div className="bg-emerald-950/20 border border-emerald-800/40 rounded-lg p-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-1.5 text-emerald-400 font-semibold mb-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>4. Recommended Action</span>
            </div>
            <p className="text-emerald-200/90 leading-relaxed text-[11.5px]">{action}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
