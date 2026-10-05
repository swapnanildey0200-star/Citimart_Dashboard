import React from "react";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { formatPercent, getGrowthColor } from "../utils/formatters";

export default function KPICard({
  title,
  value,
  lyValue = null,
  growthPct = null,
  inverse = false,
  icon: Icon = null,
  subtitle = null,
  onClick = null
}) {
  const isClickable = Boolean(onClick);

  return (
    <div
      onClick={onClick}
      className={`bg-slate-900/90 border border-slate-800 rounded-xl p-3.5 shadow-sm transition-all hover:border-slate-700/80 ${
        isClickable ? "cursor-pointer hover:bg-slate-850" : ""
      }`}
    >
      <div className="flex items-center justify-between gap-2 mb-1.5">
        <span className="text-xs font-medium uppercase tracking-wider text-slate-400 truncate">
          {title}
        </span>
        {Icon && <Icon className="w-4 h-4 text-slate-500 shrink-0" />}
      </div>

      <div className="flex items-baseline justify-between gap-2">
        <div className="text-xl font-bold tracking-tight text-white">
          {value}
        </div>

        {growthPct !== undefined && growthPct !== null && (
          <div
            className={`flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full border ${getGrowthColor(
              growthPct,
              inverse
            )}`}
          >
            {growthPct > 0 ? (
              <TrendingUp className="w-3 h-3" />
            ) : growthPct < 0 ? (
              <TrendingDown className="w-3 h-3" />
            ) : (
              <Minus className="w-3 h-3" />
            )}
            <span>{formatPercent(growthPct)}</span>
          </div>
        )}
      </div>

      {(lyValue || subtitle) && (
        <div className="mt-1.5 flex items-center justify-between text-[11px] text-slate-400">
          {lyValue && <span>LY: <strong className="text-slate-300">{lyValue}</strong></span>}
          {subtitle && <span className="truncate">{subtitle}</span>}
        </div>
      )}
    </div>
  );
}
