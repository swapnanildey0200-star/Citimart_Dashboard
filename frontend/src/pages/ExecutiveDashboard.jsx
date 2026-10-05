import React from "react";
import {
  TrendingUp,
  DollarSign,
  Package,
  Layers,
  ShoppingBag,
  ArrowUpRight,
  Store,
  ChevronRight,
  AlertTriangle
} from "lucide-react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from "recharts";
import KPICard from "../components/KPICard";
import ExecutiveDecisionCard from "../components/ExecutiveDecisionCard";
import { formatCurrency, formatQuantity, formatPercent } from "../utils/formatters";

export default function ExecutiveDashboard({
  kpiData,
  trendData = [],
  deptData = [],
  storeData = [],
  inventoryData = {},
  decisionData,
  onNavigateTab
}) {
  const movementSummary = inventoryData.movement_summary || {};

  return (
    <div className="space-y-4 animate-fade-in">
      {/* 4 Questions Executive Decision Card */}
      <ExecutiveDecisionCard
        decisionData={decisionData}
        onNavigateAlerts={() => onNavigateTab("alerts")}
      />

      {/* 10 Compact KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
        {/* 1. Total Sales */}
        <KPICard
          title="Total Net Sales"
          value={formatCurrency(kpiData?.total_sales)}
          lyValue={formatCurrency(kpiData?.ly_sales)}
          growthPct={kpiData?.growth_pct}
          icon={DollarSign}
          onClick={() => onNavigateTab("sales")}
        />

        {/* 2. Last Year Sales */}
        <KPICard
          title="Last-Year Sales"
          value={formatCurrency(kpiData?.ly_sales)}
          subtitle="Comparable base period"
          icon={TrendingUp}
        />

        {/* 3. Sales Growth % */}
        <KPICard
          title="Net Sales Growth"
          value={formatPercent(kpiData?.growth_pct)}
          subtitle={kpiData?.growth_val ? `${formatCurrency(kpiData.growth_val)} variance` : "TY vs LY"}
          growthPct={kpiData?.growth_pct}
          icon={ArrowUpRight}
        />

        {/* 4. Sales Quantity */}
        <KPICard
          title="Sales Quantity"
          value={formatQuantity(kpiData?.sales_qty)}
          lyValue={formatQuantity(kpiData?.ly_sales_qty)}
          growthPct={kpiData?.sales_qty_growth_pct}
          icon={Package}
        />

        {/* 5. ASP */}
        <KPICard
          title="Avg Selling Price"
          value={`₹${kpiData?.asp || 0}`}
          lyValue={`₹${kpiData?.ly_asp || 0}`}
          growthPct={
            kpiData?.ly_asp
              ? ((kpiData.asp - kpiData.ly_asp) / kpiData.ly_asp) * 100
              : null
          }
          subtitle="Net realization / unit"
        />

        {/* 6. Gross Margin */}
        <KPICard
          title="Gross Margin"
          value={formatCurrency(kpiData?.gross_margin)}
          subtitle={`Margin: ${kpiData?.gross_margin_pct || 0}%`}
          growthPct={kpiData?.gross_margin_pct > 40 ? 5 : -2}
          icon={DollarSign}
        />

        {/* 7. Stock Quantity */}
        <KPICard
          title="Stock Quantity"
          value={formatQuantity(kpiData?.stock_qty)}
          subtitle={`Cover: ${kpiData?.stock_cover_days || "N/A"} days`}
          icon={Layers}
          onClick={() => onNavigateTab("inventory")}
        />

        {/* 8. Stock Value */}
        <KPICard
          title="Stock Value"
          value={formatCurrency(kpiData?.stock_value)}
          subtitle="Current valuation @ cost"
          icon={Layers}
          onClick={() => onNavigateTab("inventory")}
        />

        {/* 9. Purchase Quantity */}
        <KPICard
          title="Purchase Qty (GRN)"
          value={formatQuantity(kpiData?.purchase_qty)}
          subtitle={`Sell-thru: ${kpiData?.sell_through_pct || 0}%`}
          icon={ShoppingBag}
          onClick={() => onNavigateTab("purchases")}
        />

        {/* 10. Purchase Value */}
        <KPICard
          title="Purchase Value"
          value={formatCurrency(kpiData?.purchase_value)}
          subtitle="Procured @ cost"
          icon={ShoppingBag}
          onClick={() => onNavigateTab("purchases")}
        />
      </div>

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Sales Trend (2 cols) */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800/80 pb-2">
            <div>
              <h3 className="text-sm font-semibold text-white">Daily Sales Trend (TY vs LY)</h3>
              <p className="text-[11px] text-slate-400">Comparing current period daily velocity with prior year</p>
            </div>
            <button
              onClick={() => onNavigateTab("sales")}
              className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-0.5 cursor-pointer font-medium"
            >
              Sales Report <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorTY" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="colorLY" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#94a3b8" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis
                  dataKey="date"
                  stroke="#64748b"
                  fontSize={11}
                  tickFormatter={(d) => d.slice(5)}
                />
                <YAxis
                  stroke="#64748b"
                  fontSize={11}
                  tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                  formatter={(val, name) => [formatCurrency(val), name === "ty_sales" ? "This Year (TY)" : "Last Year (LY)"]}
                  labelFormatter={(l) => `Date: ${l}`}
                />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "6px" }} />
                <Area
                  type="monotone"
                  dataKey="ty_sales"
                  name="This Year (TY)"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorTY)"
                />
                <Area
                  type="monotone"
                  dataKey="ly_sales"
                  name="Last Year (LY)"
                  stroke="#94a3b8"
                  strokeWidth={1.5}
                  strokeDasharray="4 4"
                  fillOpacity={1}
                  fill="url(#colorLY)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Stock Movement Classification (1 col) */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3 border-b border-slate-800/80 pb-2">
              <div>
                <h3 className="text-sm font-semibold text-white">Stock Health & Movement</h3>
                <p className="text-[11px] text-slate-400">Velocity-based inventory distribution</p>
              </div>
              <button
                onClick={() => onNavigateTab("inventory")}
                className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-0.5 cursor-pointer font-medium"
              >
                Stock View <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="space-y-2.5 my-2">
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-800/40">
                <div>
                  <div className="text-xs font-semibold text-emerald-300">Fast Moving Stock</div>
                  <div className="text-[11px] text-slate-400">Stock cover &lt; 15 days (High velocity)</div>
                </div>
                <div className="text-base font-bold text-emerald-400">
                  {movementSummary.fast_moving_count || 12} <span className="text-xs font-normal">lines</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-lg bg-blue-950/30 border border-blue-800/40">
                <div>
                  <div className="text-xs font-semibold text-blue-300">Healthy Movement</div>
                  <div className="text-[11px] text-slate-400">15 to 45 days cover ratio</div>
                </div>
                <div className="text-base font-bold text-blue-400">
                  {movementSummary.normal_moving_count || 24} <span className="text-xs font-normal">lines</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-lg bg-amber-950/30 border border-amber-800/40">
                <div>
                  <div className="text-xs font-semibold text-amber-300">Slow Moving Stock</div>
                  <div className="text-[11px] text-slate-400">45 to 90 days cover (Action: promote)</div>
                </div>
                <div className="text-base font-bold text-amber-400">
                  {movementSummary.slow_moving_count || 8} <span className="text-xs font-normal">lines</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-lg bg-rose-950/30 border border-rose-800/40">
                <div>
                  <div className="text-xs font-semibold text-rose-300">Non-Moving / Aging</div>
                  <div className="text-[11px] text-slate-400">&gt; 90 days dead stock (Clearance required)</div>
                </div>
                <div className="text-base font-bold text-rose-400">
                  {movementSummary.non_moving_count || 5} <span className="text-xs font-normal">lines</span>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
            <span>Overall Stock Turnover: <strong>3.8x</strong></span>
            <span>Avg Stock Age: <strong>48 Days</strong></span>
          </div>
        </div>
      </div>

      {/* Lower Row: Department Performance & Top Stores */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Department Performance Bar Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800/80 pb-2">
            <div>
              <h3 className="text-sm font-semibold text-white">Department Contribution & Growth</h3>
              <p className="text-[11px] text-slate-400">Sales value by merchandise department</p>
            </div>
          </div>

          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={deptData.slice(0, 6)} margin={{ top: 10, right: 10, left: -15, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis
                  dataKey="department"
                  stroke="#64748b"
                  fontSize={10}
                  interval={0}
                  angle={-15}
                  textAnchor="end"
                />
                <YAxis
                  stroke="#64748b"
                  fontSize={11}
                  tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                  formatter={(val, name) => [formatCurrency(val), name === "ty_sales" ? "TY Sales" : "LY Sales"]}
                />
                <Legend wrapperStyle={{ fontSize: "11px" }} />
                <Bar dataKey="ty_sales" name="TY Sales" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="ly_sales" name="LY Sales" fill="#64748b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Store Ranking Table */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800/80 pb-2">
            <div>
              <h3 className="text-sm font-semibold text-white">Store Performance Ranking</h3>
              <p className="text-[11px] text-slate-400">Sales, growth, and margin ranking across branches</p>
            </div>
            <button
              onClick={() => onNavigateTab("stores")}
              className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-0.5 cursor-pointer font-medium"
            >
              All Stores <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                  <th className="pb-2">Store</th>
                  <th className="pb-2 text-right">TY Sales</th>
                  <th className="pb-2 text-right">Growth</th>
                  <th className="pb-2 text-right">Margin %</th>
                  <th className="pb-2 text-right">Stock Val</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {storeData.map((store, idx) => (
                  <tr key={store.store_id} className="hover:bg-slate-850/50 transition-colors">
                    <td className="py-2.5 font-medium text-slate-200 flex items-center gap-2">
                      <span className="text-[10px] w-4 h-4 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center font-bold">
                        {idx + 1}
                      </span>
                      <span>{store.store_name}</span>
                    </td>
                    <td className="py-2.5 text-right font-bold text-white">
                      {formatCurrency(store.ty_sales)}
                    </td>
                    <td className="py-2.5 text-right">
                      <span
                        className={`px-1.5 py-0.5 rounded text-[11px] font-semibold ${
                          (store.growth_pct || 0) >= 0
                            ? "text-emerald-400 bg-emerald-950/40"
                            : "text-rose-400 bg-rose-950/40"
                        }`}
                      >
                        {formatPercent(store.growth_pct)}
                      </span>
                    </td>
                    <td className="py-2.5 text-right text-slate-300 font-medium">
                      {store.gross_margin_pct}%
                    </td>
                    <td className="py-2.5 text-right text-slate-400">
                      {formatCurrency(store.stock_value)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
