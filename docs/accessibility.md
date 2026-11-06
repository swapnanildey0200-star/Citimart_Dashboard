# Accessibility Standards & Target Baselines — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** A11Y-CITI-001  
**Version:** 1.1.0  
**Status:** Approved Baseline  

---

## 1. Compliance Target & Principles

The Citimart Dashboard targets **WCAG 2.1 Level AA** standards to ensure all store managers, buyers, and operations personnel can effectively navigate dashboards and review retail metrics.

### Key Objectives
1. **Perceivable:** High color contrast ratios across data visualizations, status badges, and table text.
2. **Operable:** Complete keyboard navigability across global filter dropdowns, modal windows, and data tables.
3. **Understandable:** Consistent table column headers, clear metric formulas, and descriptive error messages.
4. **Robust:** Semantic HTML elements with appropriate ARIA attributes for screen readers.

---

## 2. Color Contrast & Palette Standards

- **Text Contrast:** All body text meets or exceeds the `4.5:1` contrast ratio against background surfaces (`text-slate-800` on `bg-white`).
- **Data Visualizations:** Charts in Recharts use dual indicators (distinct stroke colors plus shape markers or tooltips) so color blindness does not inhibit data interpretation.
- **Alert Badges:** Critical (`bg-rose-50 text-rose-700`), Warning (`bg-amber-50 text-amber-700`), and Info (`bg-blue-50 text-blue-700`) badges combine color fills with text labels and Lucide status icons.

---

## 3. Keyboard Navigation & Assistive Tech

- **Tab Order:** Logical progression from Header → Navigation Tabs → Global Filter Bar → Dashboard KPI Cards → Analytical Tables.
- **Modals:** Focus is trapped inside the threshold edit modal and upload wizard until closed with Escape or the close button.
- **Data Tables:** Multi-column tables feature semantic `<th>` headers with `scope="col"` and clear `aria-sort` indicators for sorted columns.
