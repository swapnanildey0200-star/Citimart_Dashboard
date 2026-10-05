import React, { useState } from "react";
import { Download, Search, TrendingUp, TrendingDown, ArrowUpDown } from "lucide-react";
import { formatCurrency, formatQuantity, formatPercent, getGrowthColor } from "../utils/formatters";
import { exportCsvData } from "../services/api";

export default function SalesAnalysis({ deptData = [], kpiData = {} }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortField, setSortField] = useState("ty_sales");
  const [sortOrder, setSortOrder] = useState("desc");

  const handleSort = (field) => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("desc");
    }
  };

  const filteredDepts = deptData.filter((d) => {
    const q = searchTerm.toLowerCase();
    return (
      d.department.toLowerCase().includes(q) ||
      d.division.toLowerCase().includes(q)
    );
  });

  const sortedDepts = [...filteredDepts].sort((a, b) => {
    const valA = a[sortField] || 0;
    const valB = b[sortField] || 0;
    return sortOrder === "asc" ? valA - valB : valB - valA;
  });

  const handleExport = () => {
    const exportRows = sortedDepts.map((d) => ({
      Department: d.department,
      Division: d.division,
      "TY Sales (₹)": d.ty_sales,
      "LY Sales (₹)": d.ly_sales,
      "Growth (%)": d.growth_pct,
      "Growth Value (₹)": d.growth_val,
      "Contribution (%)": d.contribution_pct,
      "Sales Qty": d.ty_qty,
      "ASP (₹)": d.asp,
      "Gross Margin (₹)": d.gross_margin,
      "Margin (%)": d.gross_margin_pct
    }));
    exportCsvData("citimart_sales_analysis.csv", Object.keys(exportRows[0] || {}), exportRows);
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner & Metrics */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Sales & Category Performance</h2>
          <p className="text-xs text-slate-400">
            TY vs LY sales variance, ASP realization, gross margin contribution, and merchandise mix
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search department or division..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-950 border border-slate-800 text-slate-200 text-xs pl-8 pr-3 py-1.5 rounded-lg focus:outline-none focus:border-blue-500 w-60"
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

      {/* Summary KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Total Net Sales (TY)</div>
          <div className="text-lg font-bold text-white mt-1">{formatCurrency(kpiData?.total_sales)}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">LY: {formatCurrency(kpiData?.ly_sales)}</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Growth Variance</div>
          <div className={`text-lg font-bold mt-1 ${getGrowthColor(kpiData?.growth_pct)}`}>
            {formatPercent(kpiData?.growth_pct)}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">{formatCurrency(kpiData?.growth_val)} net diff</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Overall ASP Realization</div>
          <div className="text-lg font-bold text-white mt-1">₹{kpiData?.asp || 0}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">LY: ₹{kpiData?.ly_asp || 0}</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
          <div className="text-xs text-slate-400">Blended Gross Margin</div>
          <div className="text-lg font-bold text-emerald-400 mt-1">{kpiData?.gross_margin_pct || 0}%</div>
          <div className="text-[11px] text-slate-500 mt-0.5">{formatCurrency(kpiData?.gross_margin)} gross profit</div>
        </div>
      </div>

      {/* Detailed Sales Data Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold select-none">
                <th onClick={() => handleSort("department")} className="pb-2.5 cursor-pointer hover:text-white">
                  <div className="flex items-center gap-1">Department <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th onClick={() => handleSort("division")} className="pb-2.5 cursor-pointer hover:text-white">
                  <div className="flex items-center gap-1">Division <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th onClick={() => handleSort("ty_sales")} className="pb-2.5 text-right cursor-pointer hover:text-white">
                  <div className="flex items-center justify-end gap-1">TY Sales (₹) <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th onClick={() => handleSort("ly_sales")} className="pb-2.5 text-right cursor-pointer hover:text-white">
                  <div className="flex items-center justify-end gap-1">LY Sales (₹) <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th onClick={() => handleSort("growth_pct")} className="pb-2.5 text-right cursor-pointer hover:text-white">
                  <div className="flex items-center justify-end gap-1">Growth (%) <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th onClick={() => handleSort("contribution_pct")} className="pb-2.5 text-right cursor-pointer hover:text-white">
                  <div className="flex items-center justify-end gap-1">Contrib (%) <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th onClick={() => handleSort("ty_qty")} className="pb-2.5 text-right cursor-pointer hover:text-white">
                  <div className="flex items-center justify-end gap-1">Units Sold <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th onClick={() => handleSort("asp")} className="pb-2.5 text-right cursor-pointer hover:text-white">
                  <div className="flex items-center justify-end gap-1">ASP (₹) <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th onClick={() => handleSort("gross_margin_pct")} className="pb-2.5 text-right cursor-pointer hover:text-white">
                  <div className="flex items-center justify-end gap-1">Margin (%) <ArrowUpDown className="w-3 h-3" /></div>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {sortedDepts.map((d) => (
                <tr key={d.department} className="hover:bg-slate-850/50 transition-colors">
                  <td className="py-2.5 font-semibold text-white">{d.department}</td>
                  <td className="py-2.5 text-slate-400">{d.division}</td>
                  <td className="py-2.5 text-right font-bold text-white">{formatCurrency(d.ty_sales)}</td>
                  <td className="py-2.5 text-right text-slate-400">{formatCurrency(d.ly_sales)}</td>
                  <td className="py-2.5 text-right">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${getGrowthColor(d.growth_pct)}`}>
                      {formatPercent(d.growth_pct)}
                    </span>
                  </td>
                  <td className="py-2.5 text-right font-medium text-blue-400">{d.contribution_pct}%</td>
                  <td className="py-2.5 text-right text-slate-300 font-medium">{formatQuantity(d.ty_qty)}</td>
                  <td className="py-2.5 text-right text-slate-300">₹{d.asp}</td>
                  <td className="py-2.5 text-right font-bold text-emerald-400">{d.gross_margin_pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
