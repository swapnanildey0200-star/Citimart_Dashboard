# FEAT-002: Executive Dashboard & The 4-Question Decision Engine

**Feature ID:** FEAT-002  
**Module:** Executive Dashboard  
**Version:** 1.1.0  
**Status:** Implemented & Verified  
**Owner:** UI/UX & Analytics Team  

---

## 1. Problem & Business Value
Executive leadership and senior merchandisers require instant clarity on company-wide commercial performance without having to navigate multiple granular reports. The Executive Dashboard combines 10 high-level KPIs with an intelligent decision card that directly diagnoses retail issues and prescribes solutions.

## 2. Key Components
1. **The 4-Question Management Box:**
   - *What happened?* (e.g. "Kids Casual Apparel sales declined by 21.4%").
   - *Where did it happen?* (e.g. "Citimart Gariahat & New Market").
   - *Why did it happen?* (e.g. "Stock gap in fast-moving Boys Graphic Cotton Tees - SKU C540112").
   - *What action should be taken?* (e.g. "Expedite vendor PO and transfer 250 units from Central Warehouse").
2. **10 Executive KPI Cards:**
   - Total Net Sales (`₹`), LY Sales (`₹`), Growth % (`↑/↓`), Sales Qty, ASP (`₹`), Gross Margin %, Stock Qty, Stock Value (`₹`), Purchase Qty, Purchase Value (`₹`).
3. **TY vs LY Daily Sales Trend:** Interactive Recharts line graph overlaying current year daily sales against the same period last year.
4. **Department Contribution Chart:** Visual breakdown of sales volume and margin share across divisions and departments.
5. **Top Store Rankings:** Store leaderboard sorting locations by revenue, growth %, and stock cover.

## 3. Verification Evidence
- Endpoints verified: `/api/analytics/kpis`, `/api/analytics/decision-framework`, `/api/analytics/sales-trend`.
- Safe zero-division verified for new products/stores without last year history.

