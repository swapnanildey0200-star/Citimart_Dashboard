# FEAT-003: Inventory Ageing & Stock Velocity Analysis

**Feature ID:** FEAT-003  
**Module:** Inventory Analytics  
**Version:** 1.1.0  
**Status:** Implemented & Verified  
**Owner:** Supply Chain & Inventory Operations  

---

## 1. Problem & Business Value
Excess holding costs and dead stock erode retail profitability. This feature enables category managers to monitor stock aging across stores and identify slow-moving stock before it requires aggressive discount markdowns.

## 2. Ageing Distribution Buckets
Inventory snapshots are categorized into 5 standard retail buckets based on age since receipt:
- `0–30 days`: Fresh arrivals / active intake.
- `31–60 days`: Core inventory in prime selling window.
- `61–90 days`: Maturing inventory; monitored for deceleration.
- `91–180 days`: Slow-moving stock; candidates for promotional bundling or inter-store transfer.
- `>180 days`: Dead stock; candidates for immediate clearance or supplier return.

## 3. Stock Velocity Classification
Stock cover is calculated as:
$$\text{Stock Cover (Days)} = \frac{\text{Current Stock Quantity}}{\text{Average Daily Sales Qty (30d)}}$$

- **Fast Moving:** Cover `< 15 days` (risk of stockout).
- **Normal:** Cover `15–45 days`.
- **Slow Moving:** Cover `45–90 days`.
- **Non-Moving:** Cover `> 90 days` or zero sales in last 60 days.
- **Out of Stock:** 0 units on hand with positive historical sales velocity.

## 4. Verification Evidence
- Endpoint verified: `/api/inventory/ageing-buckets`, `/api/inventory/velocity-summary`.
- Formulas verified in `docs/acceptance-criteria.md`.

