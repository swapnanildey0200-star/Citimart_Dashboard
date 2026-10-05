import React from "react";
import { Download, Store, TrendingUp, DollarSign, Layers } from "lucide-react";
import { formatCurrency, formatPercent, getGrowthColor } from "../utils/formatters";
import { exportCsvData } from "../services/api";

export default function StoreAnalysis({ storeData = [] }) {
  const handleExport = () => {
    const exportRows = storeData.map((s, idx) => ({
      Rank: idx + 1,
      "Store ID": s.store_id,
      "Store Name": s.store_name,
      Region: s.region,
      "Store Type": s.store_type,
      "TY Sales (₹)": s.ty_sales,
      "LY Sales (₹)": s.ly_sales,
      "Growth (%)": s.growth_pct,
      "Contribution (%)": s.contribution_pct,
      "ASP (₹)": s.asp,
      "Margin (%)": s.gross_margin_pct,
      "Stock Value (₹)": s.stock_value,
      "Purchases (₹)": s.purchase_value
    }));
    exportCsvData("citimart_store_analysis.csv", Object.keys(exportRows[0] || {}), exportRows);
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Store Performance & Rankings</h2>
          <p className="text-xs text-slate-400">
            Branch comparison, regional contribution, margin yield, and inventory efficiency
          </p>
        </div>

        <button
          onClick={handleExport}
          className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export CSV</span>
        </button>
      </div>

      {/* Store Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {storeData.map((s, idx) => (
          <div key={s.store_id} className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold w-5 h-5 rounded-full bg-blue-900/60 text-blue-300 flex items-center justify-center">
                  #{idx + 1}
                </span>
                <h3 className="text-sm font-bold text-white">{s.store_name}</h3>
              </div>
              <span className="text-[10px] uppercase font-semibold text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                {s.store_type}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 my-3 text-xs">
              <div className="bg-slate-950 p-2 rounded-lg border border-slate-850">
                <div className="text-[11px] text-slate-400">TY Net Sales</div>
                <div className="text-sm font-bold text-white mt-0.5">{formatCurrency(s.ty_sales)}</div>
              </div>

              <div className="bg-slate-950 p-2 rounded-lg border border-slate-850">
                <div className="text-[11px] text-slate-400">Growth vs LY</div>
                <div className={`text-sm font-bold mt-0.5 ${getGrowthColor(s.growth_pct)}`}>
                  {formatPercent(s.growth_pct)}
                </div>
              </div>

              <div className="bg-slate-950 p-2 rounded-lg border border-slate-850">
                <div className="text-[11px] text-slate-400">Gross Margin</div>
                <div className="text-sm font-bold text-emerald-400 mt-0.5">{s.gross_margin_pct}%</div>
              </div>

              <div className="bg-slate-950 p-2 rounded-lg border border-slate-850">
                <div className="text-[11px] text-slate-400">Stock Valuation</div>
                <div className="text-sm font-bold text-slate-200 mt-0.5">{formatCurrency(s.stock_value)}</div>
              </div>
            </div>

            <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800">
              <span>Region: <strong className="text-slate-300">{s.region}</strong></span>
              <span>Contribution: <strong className="text-blue-400">{s.contribution_pct}%</strong></span>
            </div>
          </div>
        ))}
      </div>

      {/* Comprehensive Store Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm overflow-hidden">
        <h3 className="text-sm font-semibold text-white mb-3">All Branches Comparative Table</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                <th className="pb-2.5">Rank</th>
                <th className="pb-2.5">Store Name</th>
                <th className="pb-2.5">Region</th>
                <th className="pb-2.5">Format</th>
                <th className="pb-2.5 text-right">TY Sales (₹)</th>
                <th className="pb-2.5 text-right">LY Sales (₹)</th>
                <th className="pb-2.5 text-right">Growth (%)</th>
                <th className="pb-2.5 text-right">ASP (₹)</th>
                <th className="pb-2.5 text-right">Margin (%)</th>
                <th className="pb-2.5 text-right">Stock Value (₹)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {storeData.map((s, idx) => (
                <tr key={s.store_id} className="hover:bg-slate-850/50 transition-colors">
                  <td className="py-2.5 text-slate-400 font-bold">#{idx + 1}</td>
                  <td className="py-2.5 font-bold text-white">{s.store_name}</td>
                  <td className="py-2.5 text-slate-400">{s.region}</td>
                  <td className="py-2.5 text-slate-300">{s.store_type}</td>
                  <td className="py-2.5 text-right font-bold text-white">{formatCurrency(s.ty_sales)}</td>
                  <td className="py-2.5 text-right text-slate-400">{formatCurrency(s.ly_sales)}</td>
                  <td className="py-2.5 text-right">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${getGrowthColor(s.growth_pct)}`}>
                      {formatPercent(s.growth_pct)}
                    </span>
                  </td>
                  <td className="py-2.5 text-right text-slate-300">₹{s.asp}</td>
                  <td className="py-2.5 text-right font-bold text-emerald-400">{s.gross_margin_pct}%</td>
                  <td className="py-2.5 text-right text-slate-300">{formatCurrency(s.stock_value)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
