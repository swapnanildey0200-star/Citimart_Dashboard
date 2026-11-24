// Date ranges are anchored to the latest sales date in the database (not today's date),
// so the dashboard opens on the data that actually exists.

const pad = (n) => String(n).padStart(2, "0");

/** Local-time YYYY-MM-DD (toISOString shifts the day in timezones ahead of UTC, e.g. IST). */
export function toDateStr(d) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

function parse(str) {
  const [y, m, d] = str.split("-").map(Number);
  return new Date(y, m - 1, d);
}

/** { date_from, date_to } for a preset, ending on `anchor` (YYYY-MM-DD; defaults to today). */
export function presetRange(preset, anchor) {
  const end = anchor ? parse(anchor) : new Date();
  const start = new Date(end);

  if (preset === "yesterday") {
    start.setDate(end.getDate() - 1);
    return { date_from: toDateStr(start), date_to: toDateStr(start) };
  }
  if (preset === "wtd") {
    const day = end.getDay();
    start.setDate(end.getDate() - (day === 0 ? 6 : day - 1)); // Monday start
  } else if (preset === "mtd") {
    start.setDate(1);
  } else if (preset === "ytd") {
    // Financial year starts 1 April
    start.setFullYear(end.getMonth() < 3 ? end.getFullYear() - 1 : end.getFullYear(), 3, 1);
  } else if (/^last\d+$/.test(preset)) {
    start.setDate(end.getDate() - Number(preset.slice(4)) + 1);
  }
  return { date_from: toDateStr(start), date_to: toDateStr(end) };
}
