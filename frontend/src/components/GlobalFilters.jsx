import React from "react";
import { Filter, Calendar, RefreshCw, X } from "lucide-react";

export default function GlobalFilters({
  filters,
  onChange,
  onReset,
  onRefresh,
  options = {},
  isLoading = false
}) {
  const { stores = [], divisions = [], departments = [] } = options;

  const handleDatePreset = (preset) => {
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];
    
    let dateFrom = null;
    let dateTo = todayStr;

    if (preset === "yesterday") {
      const yesterday = new Date(today);
      yesterday.setDate(today.getDate() - 1);
      dateFrom = yesterday.toISOString().split('T')[0];
      dateTo = dateFrom;
    } else if (preset === "wtd") {
      const wtdStart = new Date(today);
      const day = wtdStart.getDay();
      const diff = wtdStart.getDate() - day + (day === 0 ? -6 : 1); // Monday start
      wtdStart.setDate(diff);
      dateFrom = wtdStart.toISOString().split('T')[0];
    } else if (preset === "mtd") {
      const mtdStart = new Date(today.getFullYear(), today.getMonth(), 1);
      dateFrom = mtdStart.toISOString().split('T')[0];
    } else if (preset === "ytd") {
      // Financial Year starts April 1st
      let ytdYear = today.getFullYear();
      if (today.getMonth() < 3) { // Jan, Feb, Mar
        ytdYear -= 1;
      }
      const ytdStart = new Date(ytdYear, 3, 1);
      dateFrom = ytdStart.toISOString().split('T')[0];
    }

    onChange({
      ...filters,
      date_preset: preset,
      date_from: dateFrom,
      date_to: dateTo,
      ly_date_from: null,
      ly_date_to: null
    });
  };

  const handleStoreChange = (e) => {
    const val = e.target.value;
    onChange({
      ...filters,
      stores: val ? [val] : null
    });
  };

  const handleDivisionChange = (e) => {
    const val = e.target.value;
    onChange({
      ...filters,
      divisions: val ? [val] : null,
      departments: null // reset department when division changes
    });
  };

  const handleDepartmentChange = (e) => {
    const val = e.target.value;
    onChange({
      ...filters,
      departments: val ? [val] : null
    });
  };

  const activeFilterCount =
    (filters.stores ? 1 : 0) +
    (filters.divisions ? 1 : 0) +
    (filters.departments ? 1 : 0) +
    (filters.date_preset && filters.date_preset !== "ytd" ? 1 : 0);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-3 mb-4 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3">
        {/* Date presets */}
        <div className="flex items-center gap-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
          <Calendar className="w-3.5 h-3.5 text-slate-400 ml-1.5 mr-0.5" />
          {[
            { id: "yesterday", label: "Yesterday" },
            { id: "wtd", label: "WTD" },
            { id: "mtd", label: "MTD" },
            { id: "ytd", label: "YTD (FY)" }
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => handleDatePreset(item.id)}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors cursor-pointer ${filters.date_preset === item.id
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        {/* Custom Date Range TY */}
        <div className="flex items-center gap-1.5 bg-slate-950 p-1.5 rounded-lg border border-slate-800 text-xs text-slate-200">
          <span className="font-semibold text-blue-400">TY:</span>
          <input 
            type="date" 
            className="bg-transparent outline-none cursor-pointer [&::-webkit-calendar-picker-indicator]:invert-[0.7]"
            value={filters.date_from || ""}
            onChange={(e) => onChange({ ...filters, date_preset: "custom", date_from: e.target.value })}
          />
          <span className="text-slate-500">to</span>
          <input 
            type="date" 
            className="bg-transparent outline-none cursor-pointer [&::-webkit-calendar-picker-indicator]:invert-[0.7]"
            value={filters.date_to || ""}
            onChange={(e) => onChange({ ...filters, date_preset: "custom", date_to: e.target.value })}
          />
        </div>

        {/* Custom Date Range LY */}
        <div className="flex items-center gap-1.5 bg-slate-950 p-1.5 rounded-lg border border-slate-800 text-xs text-slate-200">
          <span className="font-semibold text-orange-400">LY:</span>
          <input 
            type="date" 
            className="bg-transparent outline-none cursor-pointer [&::-webkit-calendar-picker-indicator]:invert-[0.7]"
            value={filters.ly_date_from || ""}
            onChange={(e) => onChange({ ...filters, date_preset: "custom", ly_date_from: e.target.value })}
          />
          <span className="text-slate-500">to</span>
          <input 
            type="date" 
            className="bg-transparent outline-none cursor-pointer [&::-webkit-calendar-picker-indicator]:invert-[0.7]"
            value={filters.ly_date_to || ""}
            onChange={(e) => onChange({ ...filters, date_preset: "custom", ly_date_to: e.target.value })}
          />
        </div>

        {/* Hierarchy & Store Dropdowns */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          {/* Store select */}
          <select
            value={(filters.stores && filters.stores[0]) || ""}
            onChange={handleStoreChange}
            className="bg-slate-950 border border-slate-800 text-slate-200 px-2.5 py-1.5 rounded-lg focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="">All Citimart Stores (3)</option>
            {stores.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>

          {/* Division select */}
          <select
            value={(filters.divisions && filters.divisions[0]) || ""}
            onChange={handleDivisionChange}
            className="bg-slate-950 border border-slate-800 text-slate-200 px-2.5 py-1.5 rounded-lg focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="">All Divisions</option>
            {divisions.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>

          {/* Department select */}
          <select
            value={(filters.departments && filters.departments[0]) || ""}
            onChange={handleDepartmentChange}
            className="bg-slate-950 border border-slate-800 text-slate-200 px-2.5 py-1.5 rounded-lg focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="">All Departments</option>
            {departments.map((dept) => (
              <option key={dept} value={dept}>
                {dept}
              </option>
            ))}
          </select>

          {/* Reset Filters button if any active */}
          {activeFilterCount > 0 && (
            <button
              onClick={onReset}
              className="flex items-center gap-1 text-slate-400 hover:text-rose-400 bg-slate-950 hover:bg-rose-950/30 border border-slate-800 hover:border-rose-900 px-2 py-1.5 rounded-lg transition-colors cursor-pointer"
              title="Reset all filters"
            >
              <X className="w-3.5 h-3.5" />
              <span>Reset ({activeFilterCount})</span>
            </button>
          )}

          {/* Refresh Button */}
          <button
            onClick={onRefresh}
            disabled={isLoading}
            className="flex items-center gap-1 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-2.5 py-1.5 rounded-lg transition-colors cursor-pointer disabled:opacity-50"
            title="Refresh analytics data"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
            <span>{isLoading ? "Updating..." : "Refresh"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
