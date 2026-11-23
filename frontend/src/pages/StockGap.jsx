import React, { useState, useEffect } from "react";
import { Download, Search, PackageMinus } from "lucide-react";
import { fetchStockGap, exportCsvData } from "../services/api";
import { formatCurrency, formatQuantity } from "../utils/formatters";

const STATUS_STYLE = {
  stockout: "text-rose-400 bg-rose-950/50 border border-rose-800",
  critical: "text-amber-400 bg-amber-950/50 border border-amber-800",
  low: "text-blue-400 bg-blue-950/50 border border-blue-800"
};

export default function StockGap({ filters = {} }) {
  const [data, setData] = useState(null);
  const [targetDays, setTargetDays] = useState(30);
  const [statusFilter, setStatusFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    setError("");
    fetchStockGap(filters, targetDays)
      .then((res) => !cancelled && setData(res))
      .catch((err) => !cancelled && setError(err.message))
      .finally(() => !cancelled && setIsLoading(false));
    return () => {
      cancelled = true;
    };
  }, [filters, targetDays]);

  const summary = data?.summary || {};
  const items = (data?.items || []).filter((i) => {
    const q = searchTerm.toLowerCase();
    const matchesSearch =
      i.sku.toLowerCase().includes(q) || i.name.toLowerCase().includes(q) || i.store_id.toLowerCase().includes(q);
    return matchesSearch && (statusFilter === "all" || i.status === statusFilter);
  });

  const handleExport = () => {
    const rows = items.map((i) => ({
      SKU: i.sku,
      "Product Name": i.name,
      Store: i.store_id,
      "Stock Qty": i.stock_qty,
      "Run Rate/Day": i.daily_run_rate,
      "Cover (Days)": i.cover_days,
      "Required Qty": i.required_qty,
      "Gap Qty": i.gap_qty,
      "Gap Value (₹)": i.gap_value,
      "Warehouse Qty": i.warehouse_qty,
      Status: i.status
    }));
    exportCsvData("citimart_stock_gap.csv", Object.keys(rows[0] || {}), rows);
  };

  const cards = [
    { id: "stockout", label: "Stock-outs", value: summary.stockout_count, note: "Selling, but zero on hand", color: "text-rose-400" },
    { id: "critical", label: "Critical (<7d cover)", value: summary.critical_count, note: "Will run out within a week", color: "text-amber-400" },
    { id: "low", label: `Low (<${targetDays}d cover)`, value: summary.low_count, note: "Below target cover", color: "text-blue-400" }
  ];

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Stock Gap Analysis</h2>
          <p className="text-xs text-slate-400">
            Units short of target cover, per store and SKU, ranked by sales value at risk
          </p>
        </div>
        <div className="flex items-center gap-3">
          <label className="text-xs text-slate-400 flex items-center gap-2">
            Target cover
            <select
              value={targetDays}
              onChange={(e) => setTargetDays(Number(e.target.value))}
              className="bg-slate-950 border border-slate-800 text-slate-200 text-xs px-2 py-1.5 rounded-lg focus:outline-none focus:border-blue-500"
            >
              {[15, 30, 45, 60].map((d) => (
                <option key={d} value={d}>{d} days</option>
              ))}
            </select>
          </label>
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search SKU, product or store..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-950 border border-slate-800 text-slate-200 text-xs pl-8 pr-3 py-1.5 rounded-lg focus:outline-none focus:border-blue-500 w-56"
            />
          </div>
          <button
            onClick={handleExport}
            disabled={!items.length}
            className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {error && <div className="bg-rose-950/50 border border-rose-800 rounded-xl p-3 text-xs text-rose-300">{error}</div>}

      {data && !data.has_inventory && (
        <div className="bg-amber-950/30 border border-amber-800/60 rounded-xl p-4 text-xs text-amber-200 flex items-start gap-3">
          <PackageMinus className="w-4 h-4 mt-0.5 shrink-0" />
          <span>
            No stock data found. Stock gap compares sales pace with stock on hand, so upload a stock register
            (Data Upload, Inventory) to see results.
          </span>
        </div>
      )}

      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        {cards.map((c) => (
          <button
            key={c.id}
            onClick={() => setStatusFilter(statusFilter === c.id ? "all" : c.id)}
            className={`text-left bg-slate-900 border rounded-xl p-3 cursor-pointer transition-all ${statusFilter === c.id ? "border-blue-500 ring-1 ring-blue-500" : "border-slate-800 hover:border-slate-700"}`}
          >
            <div className="text-xs text-slate-400">{c.label}</div>
            <div className={`text-lg font-bold mt-1 ${c.color}`}>{c.value ?? 0}</div>
            <div className="text-[11px] text-slate-400 mt-0.5">{c.note}</div>
          </button>
        ))}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Total Gap</div>
          <div className="text-lg font-bold text-white mt-1">{formatQuantity(summary.gap_qty)} units</div>
          <div className="text-[11px] text-slate-400 mt-0.5">{formatCurrency(summary.gap_value)} at selling price</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Lines Checked</div>
          <div className="text-lg font-bold text-white mt-1">{summary.lines_checked ?? 0}</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Store + SKU, {data?.period_days || 0}-day sales window</div>
        </div>
      </div>

      {data?.by_store?.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <h3 className="text-sm font-semibold text-white mb-2">Gap by Store</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 text-xs">
            {data.by_store.slice(0, 6).map((s) => (
              <div key={s.store_id} className="flex items-center justify-between bg-slate-950 border border-slate-800 rounded-lg px-3 py-2">
                <span className="text-slate-200 font-medium truncate mr-2">{s.store_id.replace("STR_", "")}</span>
                <span className="text-slate-400 whitespace-nowrap">
                  {s.lines} lines &middot; <strong className="text-white">{formatCurrency(s.gap_value)}</strong>
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-white">Replenishment Needs</h3>
          <span className="text-xs text-slate-400">
            {isLoading ? "Loading..." : `Showing ${items.length} items (top 200 by value)`}
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                <th className="pb-2.5">SKU</th>
                <th className="pb-2.5">Product Name</th>
                <th className="pb-2.5">Store</th>
                <th className="pb-2.5 text-right">Stock</th>
                <th className="pb-2.5 text-right">Run Rate/Day</th>
                <th className="pb-2.5 text-right">Cover (Days)</th>
                <th className="pb-2.5 text-right">Required</th>
                <th className="pb-2.5 text-right">Gap Qty</th>
                <th className="pb-2.5 text-right">Gap Value</th>
                <th className="pb-2.5 text-right">In Warehouse</th>
                <th className="pb-2.5 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {items.map((i) => (
                <tr key={`${i.store_id}_${i.sku}`} className="hover:bg-slate-850/50 transition-colors">
                  <td className="py-2.5 font-mono font-medium text-blue-400">{i.sku}</td>
                  <td className="py-2.5 font-semibold text-white">{i.name}</td>
                  <td className="py-2.5 text-slate-400">{i.store_id.replace("STR_", "")}</td>
                  <td className="py-2.5 text-right text-slate-300">{i.stock_qty}</td>
                  <td className="py-2.5 text-right text-slate-400">{i.daily_run_rate}</td>
                  <td className="py-2.5 text-right text-slate-200">{i.cover_days}d</td>
                  <td className="py-2.5 text-right text-slate-300">{i.required_qty}</td>
                  <td className="py-2.5 text-right font-bold text-white">{i.gap_qty}</td>
                  <td className="py-2.5 text-right text-slate-300">{formatCurrency(i.gap_value)}</td>
                  <td className={`py-2.5 text-right font-medium ${i.warehouse_qty >= i.gap_qty ? "text-emerald-400" : i.warehouse_qty > 0 ? "text-amber-400" : "text-slate-500"}`}>
                    {i.warehouse_qty}
                  </td>
                  <td className="py-2.5 text-right">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${STATUS_STYLE[i.status]}`}>
                      {i.status}
                    </span>
                  </td>
                </tr>
              ))}
              {!isLoading && items.length === 0 && (
                <tr>
                  <td colSpan={11} className="py-6 text-center text-slate-500">No stock gaps found for the current filters.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
