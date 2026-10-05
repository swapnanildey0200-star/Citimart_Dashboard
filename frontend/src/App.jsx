import React, { useState, useEffect, useCallback } from "react";
import Header from "./components/Header";
import GlobalFilters from "./components/GlobalFilters";
import ExecutiveDashboard from "./pages/ExecutiveDashboard";
import SalesAnalysis from "./pages/SalesAnalysis";
import InventoryAnalysis from "./pages/InventoryAnalysis";
import PurchaseAnalysis from "./pages/PurchaseAnalysis";
import ProductAnalysis from "./pages/ProductAnalysis";
import StoreAnalysis from "./pages/StoreAnalysis";
import AlertsView from "./pages/AlertsView";
import UploadView from "./pages/UploadView";
import DataQualityView from "./pages/DataQualityView";
import SettingsView from "./pages/SettingsView";
import {
  fetchKpiSummary,
  fetchSalesTrend,
  fetchDepartmentPerformance,
  fetchStorePerformance,
  fetchInventorySummary,
  fetchPurchaseSummary,
  fetchFilterOptions,
  fetchDecisionCard,
  fetchDbStatus,
  fetchAlerts
} from "./services/api";

export default function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Global Filter State
  const [filters, setFilters] = useState({
    date_preset: "ytd",
    date_from: "2026-07-01",
    date_to: "2026-09-30",
    compare_with: "LY",
    stores: null,
    divisions: null,
    departments: null
  });

  const [filterOptions, setFilterOptions] = useState({
    stores: [],
    divisions: [],
    departments: []
  });

  // Analytics Datasets
  const [kpiData, setKpiData] = useState(null);
  const [trendData, setTrendData] = useState([]);
  const [deptData, setDeptData] = useState([]);
  const [storeData, setStoreData] = useState([]);
  const [inventoryData, setInventoryData] = useState({});
  const [purchaseData, setPurchaseData] = useState({});
  const [decisionData, setDecisionData] = useState(null);
  const [dbStatus, setDbStatus] = useState(null);
  const [criticalAlertCount, setCriticalAlertCount] = useState(0);

  // Initial options & DB health load
  useEffect(() => {
    async function loadMeta() {
      try {
        const [opts, st, alerts] = await Promise.all([
          fetchFilterOptions(),
          fetchDbStatus(),
          fetchAlerts("new")
        ]);
        setFilterOptions(opts);
        setDbStatus(st);
        const crit = alerts.filter((a) => a.severity === "critical").length;
        setCriticalAlertCount(crit);
      } catch (err) {
        console.error("Error loading initial metadata:", err);
      }
    }
    loadMeta();
  }, []);

  // Main Analytics Data Loader triggered by filter change
  const loadAnalytics = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [kpi, trend, dept, stores, inv, purch, decision] = await Promise.all([
        fetchKpiSummary(filters),
        fetchSalesTrend(filters),
        fetchDepartmentPerformance(filters),
        fetchStorePerformance(filters),
        fetchInventorySummary(filters),
        fetchPurchaseSummary(filters),
        fetchDecisionCard()
      ]);

      setKpiData(kpi);
      setTrendData(trend);
      setDeptData(dept);
      setStoreData(stores);
      setInventoryData(inv);
      setPurchaseData(purch);
      setDecisionData(decision);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
      setError("Unable to connect to backend analytics service. Please verify that the backend is running.");
    } finally {
      setIsLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    loadAnalytics();
  }, [loadAnalytics]);

  const handleResetFilters = () => {
    setFilters({
      date_preset: "ytd",
      date_from: "2026-07-01",
      date_to: "2026-09-30",
      compare_with: "LY",
      stores: null,
      divisions: null,
      departments: null
    });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-blue-600 selection:text-white">
      {/* Top Header */}
      <Header
        activeTab={activeTab}
        onTabChange={setActiveTab}
        dbStatus={dbStatus}
        alertCount={criticalAlertCount}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-4">
        {/* Global Filter Bar (shown on analytical pages) */}
        {["dashboard", "sales", "inventory", "purchases", "products", "stores"].includes(activeTab) && (
          <GlobalFilters
            filters={filters}
            onChange={setFilters}
            onReset={handleResetFilters}
            onRefresh={loadAnalytics}
            options={filterOptions}
            isLoading={isLoading}
          />
        )}

        {/* Global Error Banner */}
        {error && (
          <div className="bg-rose-950/50 border border-rose-800 rounded-xl p-4 text-xs text-rose-300 mb-4 flex items-center justify-between">
            <span>{error}</span>
            <button
              onClick={loadAnalytics}
              className="bg-rose-900/60 hover:bg-rose-800 px-3 py-1 rounded text-white font-semibold cursor-pointer"
            >
              Retry
            </button>
          </div>
        )}

        {/* Tab Views */}
        {activeTab === "dashboard" && (
          <ExecutiveDashboard
            kpiData={kpiData}
            trendData={trendData}
            deptData={deptData}
            storeData={storeData}
            inventoryData={inventoryData}
            decisionData={decisionData}
            onNavigateTab={setActiveTab}
          />
        )}

        {activeTab === "sales" && (
          <SalesAnalysis deptData={deptData} kpiData={kpiData} />
        )}

        {activeTab === "inventory" && (
          <InventoryAnalysis inventoryData={inventoryData} kpiData={kpiData} />
        )}

        {activeTab === "purchases" && (
          <PurchaseAnalysis purchaseData={purchaseData} kpiData={kpiData} />
        )}

        {activeTab === "products" && (
          <ProductAnalysis filters={filters} />
        )}

        {activeTab === "stores" && (
          <StoreAnalysis storeData={storeData} />
        )}

        {activeTab === "alerts" && (
          <AlertsView onNavigateTab={setActiveTab} />
        )}

        {activeTab === "upload" && (
          <UploadView onImportComplete={loadAnalytics} />
        )}

        {activeTab === "quality" && (
          <DataQualityView />
        )}

        {activeTab === "settings" && (
          <SettingsView onDataRefresh={loadAnalytics} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-800/80 py-3 text-center text-xs text-slate-500">
        <p>Citimart Retail Analytics & Management Dashboard • Built for High-Velocity Retail Operations</p>
      </footer>
    </div>
  );
}
