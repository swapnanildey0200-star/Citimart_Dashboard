# UI Design System & Interaction Contract — Citimart Retail Dashboard

**System:** Citimart Retail Analytics & Management Dashboard  
**Document ID:** DES-CITI-001  
**Version:** 1.1.0  
**Status:** Approved & Implemented Baseline  

---

## 1. Design Philosophy: Desktop-First Retail Density

Retail merchandisers and category managers examine multi-column tables, complex hierarchies, and comparative trends side-by-side. The Citimart Dashboard is intentionally designed **desktop-first**, maximizing viewport efficiency on 1080p, 1440p, and 4K monitors while maintaining clean responsive behavior.

### Core Principles
1. **Information Density without Clutter:** Use compact padding (`px-3 py-2`), subtle borders, and tabular numerals so users can scan hundreds of SKUs without excessive scrolling.
2. **Action-Oriented Visual Hierarchy:** High-priority management questions and actionable alerts take visual precedence over passive charts.
3. **Instant Financial Comprehension:** Numbers are formatted in the Indian numbering system (`₹`, Lakhs `L`, Crores `Cr`), with immediate color-coded cues for positive growth (`emerald-600`) and contraction (`rose-600`).

---

## 2. Color Palette & Semantic Tokens

The design uses a professional enterprise slate foundation paired with semantic alert accents:

| Token | Class (Tailwind) | Hex / Value | Semantic Usage |
| :--- | :--- | :--- | :--- |
| **Surface Background** | `bg-slate-50` / `bg-slate-900` | `#F8FAFC` / `#0F172A` | Application background |
| **Card Surface** | `bg-white` / `bg-slate-800` | `#FFFFFF` / `#1E293B` | KPI cards, data tables, modals |
| **Primary Accent** | `bg-indigo-600` / `text-indigo-600` | `#4F46E5` | Active tab, primary buttons, trend lines |
| **Growth / Positive**| `text-emerald-600` / `bg-emerald-50` | `#059669` / `#ECFDF5` | Positive TY vs LY variance, high margin |
| **Decline / Negative**| `text-rose-600` / `bg-rose-50` | `#E11D48` / `#FFF1F2` | Negative growth, stockouts, critical alerts |
| **Warning / Aging** | `text-amber-600` / `bg-amber-50` | `#D97706` / `#FFFBEB` | Slow-moving stock (45-90d), pending reviews |
| **Muted Text** | `text-slate-500` | `#64748B` | Secondary labels, timestamps, metadata |
| **Borders & Dividers**| `border-slate-200` | `#E2E8F0` | Table cell borders, card outlines |

---

## 3. Typography & Numerical Formatting Contract

All numerical values representing monetary currency or retail quantities must adhere to the formatting rules implemented in `frontend/src/utils/formatters.js`:

### 3.1 Currency Formatting
- **Standard Formatting:** Prefixed with `₹`, formatted using `en-IN` locale (`₹ 1,42,500.00`).
- **Compact Financial Notation (for KPI Cards):**
  - `< 1,00,000`: Full formatted value (e.g. `₹ 48,200`)
  - `1,00,000` to `99,99,999`: Displayed in Lakhs with 2 decimals (e.g. `₹ 42.50 L`)
  - `>= 1,00,00,000`: Displayed in Crores with 2 decimals (e.g. `₹ 1.42 Cr`)

### 3.2 Percentage & Variance Formatting
- **Standard Variance:** Formatted to 1 decimal place with explicit sign (e.g. `+14.2%`, `-8.5%`).
- **Zero-Division Exception:** When Last Year (LY) is 0 and TY is positive, format as `"New Entry"` instead of `"Infinity%"` or `"NaN"`.

### 3.3 Font Selection & Alignment
- **Font Family:** Modern Sans-Serif (`Inter`, system-ui).
- **Tabular Numerals:** All numeric table cells must employ `tabular-nums` CSS so numbers align vertically across rows.
- **Table Cell Alignment:** Text columns left-aligned; all numeric and currency values strictly **right-aligned**.

---

## 4. Key UI Components

### 4.1 Header (`Header.jsx`)
- Brand identity with Citimart logo.
- 10 Navigation View Tabs with active state indicator.
- Live Database Health Badge:
  - Green pulsing dot: "Connected to MongoDB Atlas"
  - Amber dot: "Resilient Fallback Mode (In-Memory)"
  - Quick link to Reseed Demo data or open Settings.

### 4.2 Global Filter Bar (`GlobalFilters.jsx`)
- Persistent filter controls mounted across all analytical views:
  - Store Selector dropdown (`All Stores` or specific store)
  - Division Selector dropdown (`All Divisions`, `Apparel`, `Footwear`, etc.)
  - Department Selector dropdown
  - Date Range Preset buttons (`7D`, `30D`, `90D`, `TY`, `Custom`)
  - Date Range Picker when `Custom` is active.

### 4.3 Executive Decision Card (`ExecutiveDecisionCard.jsx`)
- Distinct visual container prominently positioned at top of Executive Dashboard.
- Structured according to the 4-Question Framework:
  - **1. What happened?** Highlighted anomaly pill with metric delta.
  - **2. Where did it happen?** Store and department tags.
  - **3. Why did it happen?** Root cause synthesis (e.g. SKU stock cover exhaustion).
  - **4. What action should be taken?** Concrete directive with purchase order or transfer instruction.

### 4.4 KPI Card (`KPICard.jsx`)
- Metric Title and Info Tooltip.
- Large Primary Value (e.g. `₹ 1.42 Cr`).
- Comparison Subtext (e.g. `vs LY ₹ 1.28 Cr`).
- Pill badge with dynamic growth arrow (`↑ +10.6%` or `↓ -4.2%`).

---

## 5. Responsive Breakpoints

| Breakpoint | Target Resolution | Layout Behavior |
| :--- | :--- | :--- |
| **`sm` (640px)** | Mobile devices | Stacked cards, simplified horizontal swipe tables. |
| **`md` (768px)** | Tablets | 2-column KPI grid, scrollable data tables. |
| **`lg` (1024px)** | Small laptops | 4-column KPI grid, side-by-side charts. |
| **`xl` (1280px)** | 1080p Standard Monitors | 5-column KPI grid, full multi-column hierarchy tables. |
| **`2xl` (1536px+)**| 1440p / 4K Displays | Maximum information density, expanded charts and side panels. |
