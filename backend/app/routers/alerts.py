from fastapi import APIRouter, Query, Body, HTTPException
from typing import Optional, Dict, Any
from app.services.alert_service import AlertService

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("")
async def get_alerts(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None)
):
    return await AlertService.get_alerts(status_filter=status, severity_filter=severity)

@router.patch("/{alert_id}/status")
async def update_alert_status(
    alert_id: str,
    payload: Dict[str, str] = Body(...)
):
    new_status = payload.get("status")
    if not new_status or new_status not in ["new", "acknowledged", "resolved"]:
        raise HTTPException(status_code=400, detail="Invalid status value")
    success = await AlertService.update_alert_status(alert_id, new_status)
    return {"success": success, "alert_id": alert_id, "status": new_status}

@router.get("/decision-card")
async def get_decision_card():
    return await AlertService.get_executive_decision_card()

@router.get("/rules")
async def get_rules():
    return await AlertService.get_rules()

@router.put("/rules/{rule_id}")
async def update_rule(
    rule_id: str,
    payload: Dict[str, Any] = Body(...)
):
    threshold = float(payload.get("threshold", 0.0))
    is_active = bool(payload.get("is_active", True))
    success = await AlertService.update_rule(rule_id, threshold, is_active)
    return {"success": success, "rule_id": rule_id, "threshold": threshold, "is_active": is_active}
