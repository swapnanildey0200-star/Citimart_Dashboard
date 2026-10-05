import React, { useState } from "react";
import { Download, Search, AlertCircle, Clock, CheckCircle2, ShieldAlert } from "lucide-react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { formatCurrency, formatQuantity } from "../utils/formatters";
import { exportCsvData } from "../services/api";

export default function InventoryAnalysis({ inventoryData = {}, kpiData = {} }) {
  const [filterClass, setFilterClass] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  const agingBuckets = inventoryData.aging_buckets || [];
  const items = inventoryData.items || [];
  const movementSummary = inventoryData.movement_summary || {};

  const filteredItems = items.filter((item) => {
    const matchesSearch =
      item.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesClass = filterClass === "all" || item.classification === filterClass;
    return matchesSearch && matchesClass;
  });

  const handleExport = () => {
    const exportRows = filteredItems.map((item) => ({
      SKU: item.sku,
      "Product Name": item.name,
      Store: item.store_id,
      "Stock Qty": item.stock_qty,
      "Stock Value (₹)": item.stock_value,
      "Daily Run Rate": item.daily_run_rate,
      "Stock Cover (Days)": item.cover_days,
      "Age (Days)": item.age_days,
      Classification: item.classification
    }));
    exportCsvData("citimart_inventory_analysis.csv", Object.keys(exportRows[0] || {}), exportRows);
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Inventory & Ageing Analysis</h2>
          <p className="text-xs text-slate-400">
            Stock cover ratios, aging bracket distribution, velocity-based movement, and dead-stock mitigation
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search SKU or product..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-950 border border-slate-800 text-slate-200 text-xs pl-8 pr-3 py-1.5 rounded-lg focus:outline-none focus:border-blue-500 w-56"
            />
          </div>

          <button
            onClick={handleExport}
            className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Top KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Total Stock on Hand</div>
          <div className="text-lg font-bold text-white mt-1">{formatQuantity(kpiData?.stock_qty)} units</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Valuation: {formatCurrency(kpiData?.stock_value)}</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Blended Stock Cover</div>
          <div className="text-lg font-bold text-blue-400 mt-1">{kpiData?.stock_cover_days || "N/A"} Days</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Healthy target: 30 - 45 days</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Sell-Through Rate (STR)</div>
          <div className="text-lg font-bold text-emerald-400 mt-1">{kpiData?.sell_through_pct || 0}%</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Sales / (Stock + Purchases)</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Aging Risk (&gt;90 Days)</div>
          <div className="text-lg font-bold text-rose-400 mt-1">₹1.84 Lakhs</div>
          <div className="text-[11px] text-slate-400 mt-0.5">14% of total inventory value</div>
        </div>
      </div>

      {/* Charts Row: Aging Buckets Bar Chart & Movement breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Aging Buckets Bar Chart */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800/80 pb-2">
            <div>
              <h3 className="text-sm font-semibold text-white">Stock Valuation by Aging Bracket</h3>
              <p className="text-[11px] text-slate-400">Value of stock tied up across 0-30d, 31-60d, 61-90d, 91-180d, &gt;180d</p>
            </div>
          </div>

          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={agingBuckets} margin={{ top: 10, right: 10, left: -10, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="bucket" stroke="#64748b" fontSize={11} />
                <YAxis
                  stroke="#64748b"
                  fontSize={11}
                  tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                  formatter={(val) => [formatCurrency(val), "Stock Value"]}
                />
                <Bar dataKey="stock_value" name="Stock Value (₹)" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Movement Filters & Legend */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-white mb-1">Filter by Velocity</h3>
            <p className="text-[11px] text-slate-400 mb-3">Click to filter table items below</p>

            <div className="space-y-2 text-xs">
              {[
                { id: "all", label: "All Stock Items", count: items.length, color: "text-slate-200 bg-slate-800" },
                { id: "fast_moving", label: "Fast-Moving (<15d cover)", count: movementSummary.fast_moving_count || 0, color: "text-emerald-400 bg-emerald-950/40 border border-emerald-800/60" },
                { id: "normal_moving", label: "Normal Velocity (15-45d)", count: movementSummary.normal_moving_count || 0, color: "text-blue-400 bg-blue-950/40 border border-blue-800/60" },
                { id: "slow_moving", label: "Slow-Moving (45-90d)", count: movementSummary.slow_moving_count || 0, color: "text-amber-400 bg-amber-950/40 border border-amber-800/60" },
                { id: "non_moving", label: "Non-Moving (>90d)", count: movementSummary.non_moving_count || 0, color: "text-rose-400 bg-rose-950/40 border border-rose-800/60" }
              ].map((btn) => (
                <button
                  key={btn.id}
                  onClick={() => setFilterClass(btn.id)}
                  className={`w-full flex items-center justify-between p-2 rounded-lg font-medium transition-all cursor-pointer ${
                    filterClass === btn.id ? "ring-2 ring-blue-500" : "opacity-85 hover:opacity-100"
                  } ${btn.color}`}
                >
                  <span>{btn.label}</span>
                  <span className="font-bold">{btn.count}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="mt-3 pt-2 border-t border-slate-800/80 text-[11px] text-slate-400">
            <strong>Formula Note:</strong> Stock Cover = Current Stock Qty / (90-day Sales Qty / 90 days). Aging is based on first GRC / receipt invoice date.
          </div>
        </div>
      </div>

      {/* Item-level Details Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-white">Item-Level Stock & Velocity Details</h3>
          <span className="text-xs text-slate-400">Showing {filteredItems.length} items</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                <th className="pb-2.5">SKU</th>
                <th className="pb-2.5">Product Name</th>
                <th className="pb-2.5">Store</th>
                <th className="pb-2.5 text-right">Stock Qty</th>
                <th className="pb-2.5 text-right">Stock Value (₹)</th>
                <th className="pb-2.5 text-right">Run Rate/Day</th>
                <th className="pb-2.5 text-right">Cover (Days)</th>
                <th className="pb-2.5 text-right">Age (Days)</th>
                <th className="pb-2.5 text-right">Velocity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filteredItems.map((item, idx) => (
                <tr key={`${item.sku}_${item.store_id}_${idx}`} className="hover:bg-slate-850/50 transition-colors">
                  <td className="py-2.5 font-mono font-medium text-blue-400">{item.sku}</td>
                  <td className="py-2.5 font-semibold text-white">{item.name}</td>
                  <td className="py-2.5 text-slate-400">{item.store_id.replace("STR_", "")}</td>
                  <td className="py-2.5 text-right font-bold text-white">{item.stock_qty}</td>
                  <td className="py-2.5 text-right text-slate-300">{formatCurrency(item.stock_value)}</td>
                  <td className="py-2.5 text-right text-slate-400">{item.daily_run_rate} /d</td>
                  <td className="py-2.5 text-right font-medium text-slate-200">
                    {item.cover_days > 365 ? "> 365d" : `${item.cover_days}d`}
                  </td>
                  <td className="py-2.5 text-right text-slate-400">{item.age_days}d</td>
                  <td className="py-2.5 text-right">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                        item.classification === "fast_moving"
                          ? "text-emerald-400 bg-emerald-950/50 border border-emerald-800"
                          : item.classification === "slow_moving"
                          ? "text-amber-400 bg-amber-950/50 border border-amber-800"
                          : item.classification === "non_moving"
                          ? "text-rose-400 bg-rose-950/50 border border-rose-800"
                          : "text-blue-400 bg-blue-950/50 border border-blue-800"
                      }`}
                    >
                      {item.classification.replace("_", " ")}
                    </span>
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
