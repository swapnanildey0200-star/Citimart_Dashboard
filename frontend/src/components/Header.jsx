import React from "react";
import {
  LayoutDashboard,
  TrendingUp,
  Boxes,
  ShoppingBag,
  Tag,
  Store,
  Bell,
  UploadCloud,
  CheckCheck,
  Settings,
  Database,
  Calendar
} from "lucide-react";

export const NAV_ITEMS = [
  { id: "dashboard", label: "Executive Dashboard", icon: LayoutDashboard },
  { id: "sales", label: "Sales Analysis", icon: TrendingUp },
  { id: "inventory", label: "Inventory Analysis", icon: Boxes },
  { id: "purchases", label: "Purchases", icon: ShoppingBag },
  { id: "products", label: "Product Analysis", icon: Tag },
  { id: "stores", label: "Store Analysis", icon: Store },
  { id: "alerts", label: "Alerts & Actions", icon: Bell },
  { id: "upload", label: "Data Upload", icon: UploadCloud },
  { id: "quality", label: "Data Quality", icon: CheckCheck },
  { id: "settings", label: "Settings", icon: Settings },
];

export default function Header({ activeTab, onTabChange, dbStatus, alertCount = 0 }) {
  const isDbConnected = dbStatus?.status === "connected";

  return (
    <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-30">
      {/* Top utility row */}
      <div className="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between border-b border-slate-800/60">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center shadow-md shadow-blue-500/20">
            <span className="font-extrabold text-white text-base tracking-tighter">CM</span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-sm font-bold text-white tracking-tight">
                CITIMART RETAIL INTELLIGENCE
              </h1>
              <span className="text-[10px] bg-blue-900/40 text-blue-300 border border-blue-700/50 px-1.5 py-0.2 rounded font-mono font-semibold">
                v1.0
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Management Decision & Performance Analytics System
            </p>
          </div>
        </div>

        {/* Status badges */}
        <div className="flex items-center gap-3 text-xs">
          <div className="hidden sm:flex items-center gap-1.5 text-slate-400 bg-slate-950 px-2.5 py-1 rounded-md border border-slate-800">
            <Calendar className="w-3.5 h-3.5 text-blue-400" />
            <span>As on: <strong>30 Sep 2026</strong></span>
          </div>

          <div
            onClick={() => onTabChange("settings")}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-md border border-slate-800 bg-slate-950 cursor-pointer hover:border-slate-700 transition-colors"
            title={`Database: ${dbStatus?.mode || "checking..."}`}
          >
            <Database className="w-3.5 h-3.5 text-slate-400" />
            <div className="flex items-center gap-1.5">
              <span
                className={`w-2 h-2 rounded-full ${
                  isDbConnected ? "bg-emerald-400 animate-pulse" : "bg-emerald-500"
                }`}
              />
              <span className="text-[11px] font-medium text-slate-300">
                {isDbConnected ? "MongoDB Atlas" : "Embedded Store"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 overflow-x-auto scrollbar-none">
        <nav className="flex items-center gap-1 py-1.5 min-w-max text-xs">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            const hasAlertBadge = item.id === "alerts" && alertCount > 0;

            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all cursor-pointer ${
                  isActive
                    ? "bg-blue-600/90 text-white shadow-sm shadow-blue-500/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>

                {hasAlertBadge && (
                  <span className="ml-1 text-[10px] bg-rose-500 text-white px-1.5 py-0.2 rounded-full font-bold">
                    {alertCount}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
