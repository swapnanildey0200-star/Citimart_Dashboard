const API_BASE = "/api";

export async function fetchKpiSummary(filters = {}) {
  const res = await fetch(`${API_BASE}/analytics/kpi-summary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters)
  });
  if (!res.ok) throw new Error("Failed to load KPI summary");
  return res.json();
}

export async function fetchSalesTrend(filters = {}) {
  const res = await fetch(`${API_BASE}/analytics/sales-trend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters)
  });
  if (!res.ok) throw new Error("Failed to load sales trend");
  return res.json();
}

export async function fetchDepartmentPerformance(filters = {}) {
  const res = await fetch(`${API_BASE}/analytics/department-performance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters)
  });
  if (!res.ok) throw new Error("Failed to load department performance");
  return res.json();
}

export async function fetchStorePerformance(filters = {}) {
  const res = await fetch(`${API_BASE}/analytics/store-performance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters)
  });
  if (!res.ok) throw new Error("Failed to load store performance");
  return res.json();
}

export async function fetchProductRankings(filters = {}, limit = 10) {
  const res = await fetch(`${API_BASE}/analytics/product-rankings?limit=${limit}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters)
  });
  if (!res.ok) throw new Error("Failed to load product rankings");
  return res.json();
}

export async function fetchInventorySummary(filters = {}) {
  const res = await fetch(`${API_BASE}/inventory/summary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters)
  });
  if (!res.ok) throw new Error("Failed to load inventory summary");
  return res.json();
}

export async function fetchPurchaseSummary(filters = {}) {
  const res = await fetch(`${API_BASE}/purchases/summary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters)
  });
  if (!res.ok) throw new Error("Failed to load purchase summary");
  return res.json();
}

export async function fetchFilterOptions() {
  const res = await fetch(`${API_BASE}/analytics/filter-options`);
  if (!res.ok) throw new Error("Failed to load filter options");
  return res.json();
}

export async function fetchDecisionCard() {
  const res = await fetch(`${API_BASE}/alerts/decision-card`);
  if (!res.ok) throw new Error("Failed to load decision card");
  return res.json();
}

export async function fetchAlerts(status = null, severity = null) {
  let url = `${API_BASE}/alerts`;
  const params = [];
  if (status) params.push(`status=${status}`);
  if (severity) params.push(`severity=${severity}`);
  if (params.length > 0) url += `?${params.join("&")}`;
  
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to load alerts");
  return res.json();
}

export async function updateAlertStatus(alertId, newStatus) {
  const res = await fetch(`${API_BASE}/alerts/${alertId}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: newStatus })
  });
  if (!res.ok) throw new Error("Failed to update alert status");
  return res.json();
}

export async function fetchAlertRules() {
  const res = await fetch(`${API_BASE}/alerts/rules`);
  if (!res.ok) throw new Error("Failed to load alert rules");
  return res.json();
}

export async function updateAlertRule(ruleId, threshold, isActive) {
  const res = await fetch(`${API_BASE}/alerts/rules/${ruleId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ threshold, is_active: isActive })
  });
  if (!res.ok) throw new Error("Failed to update alert rule");
  return res.json();
}

export async function uploadFilePreview(file, dataType) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("data_type", dataType);

  const res = await fetch(`${API_BASE}/upload/preview`, {
    method: "POST",
    body: formData
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Upload preview failed");
  }
  return res.json();
}

export async function validateUploadData(file, dataType, mapping, headerRowIdx = 1) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("data_type", dataType);
  formData.append("mapping", JSON.stringify(mapping));
  formData.append("header_row_idx", headerRowIdx);

  const res = await fetch(`${API_BASE}/upload/validate`, {
    method: "POST",
    body: formData
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Validation failed");
  }
  return res.json();
}

export async function commitUploadData(payload) {
  const res = await fetch(`${API_BASE}/upload/commit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Commit import failed");
  }
  return res.json();
}

export async function fetchImportHistory() {
  const res = await fetch(`${API_BASE}/upload/history`);
  if (!res.ok) throw new Error("Failed to load import history");
  return res.json();
}

export async function fetchDbStatus() {
  const res = await fetch(`${API_BASE}/settings/db-status`);
  if (!res.ok) throw new Error("Failed to load database status");
  return res.json();
}

export async function triggerSeedData() {
  const res = await fetch(`${API_BASE}/settings/seed-data`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to seed database");
  return res.json();
}

export async function fetchMetricGlossary() {
  const res = await fetch(`${API_BASE}/settings/metric-glossary`);
  if (!res.ok) throw new Error("Failed to load metric glossary");
  return res.json();
}

export async function exportCsvData(filename, columns, data) {
  const res = await fetch(`${API_BASE}/export/csv`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filename, columns, data })
  });
  if (!res.ok) throw new Error("Failed to export CSV");
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}
