import React, { useState, useEffect } from "react";
import { Download, Search, Tag, ArrowUpRight, TrendingDown } from "lucide-react";
import { fetchProductRankings, exportCsvData } from "../services/api";
import { formatCurrency, formatQuantity, formatPercent, getGrowthColor } from "../utils/formatters";

export default function ProductAnalysis({ filters = {} }) {
  const [productData, setProductData] = useState({ top_products: [], bottom_products: [] });
  const [activeTab, setActiveTab] = useState("top");
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      try {
        const res = await fetchProductRankings(filters, 20);
        setProductData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [filters]);

  const list = activeTab === "top" ? productData.top_products : productData.bottom_products;
  const filteredList = list.filter((p) =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.department.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleExport = () => {
    const exportRows = filteredList.map((p) => ({
      SKU: p.sku,
      "Product Name": p.name,
      Division: p.division,
      Department: p.department,
      Brand: p.brand,
      "MRP (₹)": p.mrp,
      "TY Sales (₹)": p.ty_sales,
      "LY Sales (₹)": p.ly_sales,
      "Growth (%)": p.growth_pct,
      "Units Sold": p.ty_qty,
      "Gross Margin (₹)": p.gross_margin,
      "Margin (%)": p.gross_margin_pct
    }));
    exportCsvData(`citimart_${activeTab}_products.csv`, Object.keys(exportRows[0] || {}), exportRows);
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Product & SKU Performance</h2>
          <p className="text-xs text-slate-400">
            Performance rankings, top revenue contributors, margin yield, and weak SKU diagnostics
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search SKU or name..."
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

      {/* Tabs: Top Performers vs Bottom Performers */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab("top")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
            activeTab === "top"
              ? "bg-emerald-600 text-white shadow-sm"
              : "text-slate-400 hover:text-white bg-slate-900"
          }`}
        >
          <ArrowUpRight className="w-3.5 h-3.5" />
          <span>Top Revenue Generators</span>
        </button>

        <button
          onClick={() => setActiveTab("bottom")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
            activeTab === "bottom"
              ? "bg-rose-600 text-white shadow-sm"
              : "text-slate-400 hover:text-white bg-slate-900"
          }`}
        >
          <TrendingDown className="w-3.5 h-3.5" />
          <span>Underperforming / Weak SKUs</span>
        </button>
      </div>

      {/* Products Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                <th className="pb-2.5">SKU</th>
                <th className="pb-2.5">Product Name</th>
                <th className="pb-2.5">Department</th>
                <th className="pb-2.5">Brand</th>
                <th className="pb-2.5 text-right">MRP (₹)</th>
                <th className="pb-2.5 text-right">TY Sales (₹)</th>
                <th className="pb-2.5 text-right">LY Sales (₹)</th>
                <th className="pb-2.5 text-right">Growth (%)</th>
                <th className="pb-2.5 text-right">Units Sold</th>
                <th className="pb-2.5 text-right">Margin (%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filteredList.map((p) => (
                <tr key={p.sku} className="hover:bg-slate-850/50 transition-colors">
                  <td className="py-2.5 font-mono font-medium text-blue-400">{p.sku}</td>
                  <td className="py-2.5 font-semibold text-white">{p.name}</td>
                  <td className="py-2.5 text-slate-400">{p.department}</td>
                  <td className="py-2.5 text-slate-300">{p.brand}</td>
                  <td className="py-2.5 text-right text-slate-300">₹{p.mrp}</td>
                  <td className="py-2.5 text-right font-bold text-white">{formatCurrency(p.ty_sales)}</td>
                  <td className="py-2.5 text-right text-slate-400">{formatCurrency(p.ly_sales)}</td>
                  <td className="py-2.5 text-right">
                    <span className={`px-1.5 py-0.5 rounded text-[11px] font-semibold border ${getGrowthColor(p.growth_pct)}`}>
                      {formatPercent(p.growth_pct)}
                    </span>
                  </td>
                  <td className="py-2.5 text-right text-slate-300 font-medium">{formatQuantity(p.ty_qty)}</td>
                  <td className="py-2.5 text-right font-bold text-emerald-400">{p.gross_margin_pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
