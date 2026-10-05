import React, { useState, useEffect } from "react";
import {
  AlertCircle,
  Bell,
  CheckCircle,
  Settings2,
  Clock,
  MapPin,
  ExternalLink,
  ShieldAlert,
  Sliders
} from "lucide-react";
import { fetchAlerts, updateAlertStatus, fetchAlertRules, updateAlertRule } from "../services/api";

export default function AlertsView({ onNavigateTab }) {
  const [alerts, setAlerts] = useState([]);
  const [rules, setRules] = useState([]);
  const [showRulesModal, setShowRulesModal] = useState(false);
  const [filterSeverity, setFilterSeverity] = useState("all");
  const [filterStatus, setFilterStatus] = useState("all");
  const [isLoading, setIsLoading] = useState(false);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const alertsRes = await fetchAlerts();
      const rulesRes = await fetchAlertRules();
      setAlerts(alertsRes);
      setRules(rulesRes);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleStatusChange = async (alertId, newStatus) => {
    try {
      await updateAlertStatus(alertId, newStatus);
      setAlerts(
        alerts.map((a) =>
          a.alert_id === alertId ? { ...a, status: newStatus } : a
        )
      );
    } catch (err) {
      alert("Failed to update status");
    }
  };

  const handleRuleSave = async (ruleId, threshold, isActive) => {
    try {
      await updateAlertRule(ruleId, threshold, isActive);
      loadData();
    } catch (err) {
      alert("Failed to update rule");
    }
  };

  const filteredAlerts = alerts.filter((a) => {
    const matchesSev = filterSeverity === "all" || a.severity === filterSeverity;
    const matchesStat = filterStatus === "all" || a.status === filterStatus;
    return matchesSev && matchesStat;
  });

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">Management Alerts & Prescriptive Actions</h2>
          <p className="text-xs text-slate-400">
            Rule-based intelligence answering What, Where, Why, and What action to take
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowRulesModal(true)}
            className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-700 transition-colors cursor-pointer"
          >
            <Sliders className="w-3.5 h-3.5" />
            <span>Configure Thresholds</span>
          </button>
        </div>
      </div>

      {/* Filter Chips */}
      <div className="flex flex-wrap items-center gap-3 text-xs">
        <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-lg border border-slate-800">
          <span className="text-slate-500 px-2 font-medium">Severity:</span>
          {["all", "critical", "warning"].map((sev) => (
            <button
              key={sev}
              onClick={() => setFilterSeverity(sev)}
              className={`px-2.5 py-1 rounded font-medium cursor-pointer ${
                filterSeverity === sev ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
              }`}
            >
              {sev.toUpperCase()}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-lg border border-slate-800">
          <span className="text-slate-500 px-2 font-medium">Status:</span>
          {["all", "new", "acknowledged", "resolved"].map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-2.5 py-1 rounded font-medium cursor-pointer ${
                filterStatus === st ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
              }`}
            >
              {st.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Alert Cards List */}
      <div className="space-y-3">
        {filteredAlerts.length === 0 ? (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-400">
            <CheckCircle className="w-8 h-8 mx-auto text-emerald-400 mb-2" />
            <p className="text-sm font-semibold text-white">No Active Alerts</p>
            <p className="text-xs text-slate-500">All retail metrics are within configured safe thresholds.</p>
          </div>
        ) : (
          filteredAlerts.map((alert) => {
            const isCritical = alert.severity === "critical";

            return (
              <div
                key={alert.alert_id}
                className={`bg-slate-900 rounded-xl p-4 shadow-sm border transition-all ${
                  isCritical
                    ? "border-rose-900/60 bg-gradient-to-r from-slate-900 via-rose-950/10 to-slate-900"
                    : "border-amber-900/60 bg-gradient-to-r from-slate-900 via-amber-950/10 to-slate-900"
                }`}
              >
                {/* Header row */}
                <div className="flex flex-wrap items-center justify-between gap-2 mb-3 border-b border-slate-800/80 pb-2.5">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider border ${
                        isCritical
                          ? "bg-rose-500/20 text-rose-300 border-rose-500/40"
                          : "bg-amber-500/20 text-amber-300 border-amber-500/40"
                      }`}
                    >
                      {alert.severity}
                    </span>
                    <h3 className="text-sm font-bold text-white">{alert.title}</h3>
                  </div>

                  <div className="flex items-center gap-2">
                    <select
                      value={alert.status}
                      onChange={(e) => handleStatusChange(alert.alert_id, e.target.value)}
                      className="bg-slate-950 border border-slate-800 text-slate-300 text-xs px-2 py-1 rounded cursor-pointer"
                    >
                      <option value="new">New</option>
                      <option value="acknowledged">Acknowledged</option>
                      <option value="resolved">Resolved</option>
                    </select>

                    <button
                      onClick={() => onNavigateTab(alert.target_page || "sales")}
                      className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 bg-slate-950 px-2.5 py-1 rounded border border-slate-800 cursor-pointer"
                    >
                      <span>Analyze</span>
                      <ExternalLink className="w-3 h-3" />
                    </button>
                  </div>
                </div>

                {/* 4 Core Questions Grid */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
                  <div className="bg-slate-950/80 p-2.5 rounded-lg border border-slate-850">
                    <div className="text-[11px] font-semibold text-amber-400 mb-1">1. What Happened?</div>
                    <p className="text-slate-200 leading-relaxed text-[11.5px]">{alert.what_happened}</p>
                  </div>

                  <div className="bg-slate-950/80 p-2.5 rounded-lg border border-slate-850">
                    <div className="text-[11px] font-semibold text-blue-400 mb-1">2. Where?</div>
                    <p className="text-slate-200 leading-relaxed text-[11.5px]">{alert.where_happened}</p>
                  </div>

                  <div className="bg-slate-950/80 p-2.5 rounded-lg border border-slate-850">
                    <div className="text-[11px] font-semibold text-purple-400 mb-1">3. Why?</div>
                    <p className="text-slate-200 leading-relaxed text-[11.5px]">{alert.why_happened}</p>
                  </div>

                  <div className="bg-emerald-950/30 p-2.5 rounded-lg border border-emerald-800/40">
                    <div className="text-[11px] font-semibold text-emerald-400 mb-1">4. Recommended Action</div>
                    <p className="text-emerald-200/90 leading-relaxed text-[11.5px]">{alert.action_recommended}</p>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Rules Config Modal */}
      {showRulesModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 max-w-2xl w-full shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-base font-bold text-white">Configure Retail Alert Rules</h3>
                <p className="text-xs text-slate-400">Set sensitivity thresholds for automated risk detection</p>
              </div>
              <button
                onClick={() => setShowRulesModal(false)}
                className="text-slate-400 hover:text-white text-sm font-bold px-2 py-1 rounded bg-slate-800"
              >
                ✕
              </button>
            </div>

            <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
              {rules.map((rule) => (
                <div key={rule.rule_id} className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-center justify-between gap-3 text-xs">
                  <div>
                    <div className="font-semibold text-white">{rule.name}</div>
                    <div className="text-[11px] text-slate-400">Metric: {rule.metric} ({rule.condition})</div>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1.5">
                      <span className="text-slate-400">Threshold:</span>
                      <input
                        type="number"
                        defaultValue={rule.threshold}
                        onBlur={(e) => handleRuleSave(rule.rule_id, parseFloat(e.target.value), rule.is_active)}
                        className="bg-slate-900 border border-slate-700 text-white w-20 px-2 py-1 rounded text-right"
                      />
                    </div>

                    <label className="flex items-center gap-1.5 cursor-pointer">
                      <input
                        type="checkbox"
                        defaultChecked={rule.is_active}
                        onChange={(e) => handleRuleSave(rule.rule_id, rule.threshold, e.target.checked)}
                        className="rounded bg-slate-900 border-slate-700 text-blue-600"
                      />
                      <span className="text-slate-300">Active</span>
                    </label>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-end pt-2 border-t border-slate-800">
              <button
                onClick={() => setShowRulesModal(false)}
                className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg cursor-pointer"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
