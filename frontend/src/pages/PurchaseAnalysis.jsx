import React from "react";
import { Download, ShoppingBag, Truck, DollarSign, AlertTriangle } from "lucide-react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { formatCurrency, formatQuantity } from "../utils/formatters";
import { exportCsvData } from "../services/api";

export default function PurchaseAnalysis({ purchaseData = {}, kpiData = {} }) {
  const vendors = purchaseData.vendor_performance || [];
  const pVsS = purchaseData.purchase_vs_sales || {};
  const recentPOs = purchaseData.recent_pos || [];

  const handleExport = () => {
    const exportRows = vendors.map((v) => ({
      "Vendor ID": v.vendor_id,
      "Vendor Name": v.vendor_name,
      Category: v.category,
      "PO Count": v.po_count,
      "Purchase Qty": v.purchase_qty,
      "Purchase Value (₹)": v.purchase_value,
      "Concentration (%)": v.concentration_pct
    }));
    exportCsvData("citimart_vendor_purchases.csv", Object.keys(exportRows[0] || {}), exportRows);
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Procurement & Vendor Analysis</h2>
          <p className="text-xs text-slate-400">
            Goods Receive Register (GRN), vendor concentration, and purchase vs sales intake ratios
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

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Total Purchase Value</div>
          <div className="text-lg font-bold text-white mt-1">{formatCurrency(pVsS.purchase_value || kpiData.purchase_value)}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Total GRN intake</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Purchase vs Sales Ratio</div>
          <div className="text-lg font-bold text-blue-400 mt-1">{pVsS.value_ratio || "0.0"}x</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Purchases (₹) / Sales (₹)</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Active Supply Vendors</div>
          <div className="text-lg font-bold text-emerald-400 mt-1">{vendors.length} Vendors</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Across apparel & appliances</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Total Received Qty</div>
          <div className="text-lg font-bold text-white mt-1">{formatQuantity(pVsS.purchase_qty || kpiData.purchase_qty)} units</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Units received into stores</div>
        </div>
      </div>

      {/* Vendor Concentration Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
        <h3 className="text-sm font-semibold text-white mb-1">Top Vendor Procurement Intake (₹)</h3>
        <p className="text-[11px] text-slate-400 mb-3">Concentration of purchases among registered vendors</p>
        <div className="h-60 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={vendors} margin={{ top: 10, right: 10, left: -10, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="vendor_name" stroke="#64748b" fontSize={10} interval={0} angle={-15} textAnchor="end" />
              <YAxis stroke="#64748b" fontSize={11} tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                formatter={(val) => [formatCurrency(val), "Purchase Value"]}
              />
              <Bar dataKey="purchase_value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Vendor Performance Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm overflow-hidden">
        <h3 className="text-sm font-semibold text-white mb-3">Vendor Scorecard & Concentration</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                <th className="pb-2.5">Vendor</th>
                <th className="pb-2.5">Category</th>
                <th className="pb-2.5 text-right">PO Count</th>
                <th className="pb-2.5 text-right">Qty Received</th>
                <th className="pb-2.5 text-right">Purchase Value (₹)</th>
                <th className="pb-2.5 text-right">Concentration (%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {vendors.map((v) => (
                <tr key={v.vendor_id} className="hover:bg-slate-850/50 transition-colors">
                  <td className="py-2.5 font-semibold text-white">{v.vendor_name}</td>
                  <td className="py-2.5 text-slate-400">{v.category}</td>
                  <td className="py-2.5 text-right text-slate-300">{v.po_count}</td>
                  <td className="py-2.5 text-right text-slate-300 font-medium">{formatQuantity(v.purchase_qty)}</td>
                  <td className="py-2.5 text-right font-bold text-white">{formatCurrency(v.purchase_value)}</td>
                  <td className="py-2.5 text-right font-bold text-blue-400">{v.concentration_pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
