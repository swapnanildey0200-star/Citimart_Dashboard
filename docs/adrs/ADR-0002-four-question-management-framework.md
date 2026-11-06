# ADR-0002: The 4-Question Management Framework for Retail Actionability

**Status:** Accepted  
**Date:** 2026-10-22  
**Author:** Citimart Product & Operations Team  
**Supercedes:** None  

---

## 1. Context & Problem Statement

Conventional retail dashboards present charts, graphs, and metric numbers (e.g. "Total Sales ₹ 1.42 Cr, -12% vs LY"). Retail store managers and category buyers frequently struggle to translate raw charts into concrete merchandise actions. They must manually cross-reference store lists, inventory cover reports, and vendor registers to determine why revenue dropped and what purchase orders to place.

## 2. Decision

We integrated **The 4-Question Management Framework** directly into the core analytical engine (`AnalyticsService.get_decision_framework()`) and the top of the Executive Dashboard (`ExecutiveDecisionCard.jsx`):

1. **What happened?** (Identifies the largest commercial anomaly or variance delta across merchandise divisions).
2. **Where did it happen?** (Isolates specific stores or sales channels driving the anomaly).
3. **Why did it happen?** (Pinpoints the root operational cause, such as fast-runner stockout, high ageing dead stock, or delayed vendor PO).
4. **What action should be taken?** (Prescribes an exact operational directive, such as replenishing X units from the central warehouse or expediting a specific vendor PO).

## 3. Consequences

### Positive
- Bridges the gap between passive reporting and proactive management decision-making.
- Provides immediate executive briefing on dashboard open without requiring manual drilldown.
- Enhances collaboration between store operations and central category buyers.

### Negative / Tradeoffs
- Requires synthesis logic in `AnalyticsService` to evaluate multiple data points across sales and inventory.

