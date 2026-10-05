from typing import List, Dict, Any, Optional
from datetime import datetime
from app.database import db_manager

class AlertService:
    @staticmethod
    async def get_alerts(status_filter: Optional[str] = None, severity_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        alerts_coll = db_manager.get_collection("generated_alerts")
        query: Dict[str, Any] = {}
        if status_filter:
            query["status"] = status_filter
        if severity_filter:
            query["severity"] = severity_filter
        
        alerts = await alerts_coll.find(query)
        # Sort critical first, then warning, then by date
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        return sorted(alerts, key=lambda a: (severity_order.get(a.get("severity", "info"), 3), a.get("created_at", "")))

    @staticmethod
    async def update_alert_status(alert_id: str, new_status: str) -> bool:
        alerts_coll = db_manager.get_collection("generated_alerts")
        return await alerts_coll.update_one({"alert_id": alert_id}, {"$set": {"status": new_status}})

    @staticmethod
    async def get_rules() -> List[Dict[str, Any]]:
        rules_coll = db_manager.get_collection("alert_rules")
        return await rules_coll.find({})

    @staticmethod
    async def update_rule(rule_id: str, threshold: float, is_active: bool) -> bool:
        rules_coll = db_manager.get_collection("alert_rules")
        return await rules_coll.update_one(
            {"rule_id": rule_id},
            {"$set": {"threshold": threshold, "is_active": is_active}}
        )

    @staticmethod
    async def get_executive_decision_card() -> Dict[str, Any]:
        """Provides high-level concise What / Where / Why / Action summary for executive view."""
        alerts = await AlertService.get_alerts(status_filter="new")
        critical_alerts = [a for a in alerts if a.get("severity") == "critical"]
        
        if critical_alerts:
            top_critical = critical_alerts[0]
            return {
                "what": top_critical.get("what_happened", "Sales volatility detected across key retail categories."),
                "where": top_critical.get("where_happened", "Flagship branches & high-traffic regional stores."),
                "why": top_critical.get("why_happened", "Inventory stock gap in fast-moving lines and high aging in non-seasonal lines."),
                "action": top_critical.get("action_recommended", "Reallocate stock from central depot and trigger flash promotional clearance for aged SKUs."),
                "total_alerts": len(alerts),
                "critical_count": len(critical_alerts)
            }
        
        return {
            "what": "Retail operations stable across branches; net sales on track with comparable period.",
            "where": "All stores maintaining healthy cover ratios.",
            "why": "Balanced sell-through rate and steady vendor deliveries.",
            "action": "Maintain normal procurement schedule and review weekend promotional calendar.",
            "total_alerts": len(alerts),
            "critical_count": 0
        }
