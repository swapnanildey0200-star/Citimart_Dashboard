/**
 * Currency & Number Formatting Helpers for Citimart Dashboard
 */

export function formatCurrency(amount, format = "lakh_crore") {
  if (amount === null || amount === undefined || isNaN(amount)) return "₹0";

  const num = Math.abs(amount);
  const sign = amount < 0 ? "-" : "";

  if (format === "lakh_crore") {
    if (num >= 10000000) {
      return `${sign}₹${(num / 10000000).toFixed(2)} Cr`;
    } else if (num >= 100000) {
      return `${sign}₹${(num / 100000).toFixed(2)} L`;
    } else if (num >= 1000) {
      return `${sign}₹${(num / 1000).toFixed(1)} K`;
    }
    return `${sign}₹${num.toFixed(0)}`;
  }

  return `${sign}₹${num.toLocaleString("en-IN")}`;
}

export function formatQuantity(qty) {
  if (qty === null || qty === undefined || isNaN(qty)) return "0";
  const num = Math.abs(qty);
  const sign = qty < 0 ? "-" : "";

  if (num >= 100000) {
    return `${sign}${(num / 100000).toFixed(2)} L`;
  } else if (num >= 1000) {
    return `${sign}${(num / 1000).toFixed(1)} K`;
  }
  return `${sign}${num.toLocaleString("en-IN")}`;
}

export function formatPercent(val) {
  if (val === null || val === undefined) return "New";
  if (isNaN(val)) return "0.0%";
  const sign = val > 0 ? "+" : "";
  return `${sign}${val.toFixed(1)}%`;
}

export function getGrowthColor(val, inverse = false) {
  if (val === null || val === undefined) return "text-blue-400 bg-blue-900/30 border-blue-800";
  if (val === 0) return "text-slate-400 bg-slate-800 border-slate-700";

  const isPositive = inverse ? val < 0 : val > 0;
  return isPositive
    ? "text-emerald-400 bg-emerald-950/40 border-emerald-800/60"
    : "text-rose-400 bg-rose-950/40 border-rose-800/60";
}

/**
 * Formats a stored timestamp in the viewer's local time (YYYY-MM-DD HH:mm).
 * The backend stores UTC without a zone suffix, so a bare ISO string is treated as UTC.
 */
export function formatLocalDateTime(iso) {
  if (!iso) return "";
  const hasZone = /(Z|[+-]\d{2}:?\d{2})$/.test(iso);
  const d = new Date(hasZone ? iso : `${iso}Z`);
  if (isNaN(d.getTime())) return iso;
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}
