# Power BI Dashboard Specification

**Project**: Customer Value Intelligence — D2C Fashion Brand  
**Prepared by**: Nikhil Kumar  
**Date**: June 2026

---

## Overview

This document provides step-by-step instructions to recreate the four-panel founder dashboard in Power BI Desktop using the exported CSV data files.

---

## Data Sources

Import the following CSV files into Power BI (Get Data → Text/CSV):

| File | Location | Purpose |
|------|----------|---------|
| `customer_features.csv` | Root directory | Master customer table |
| `dashboard_pyramid.csv` | `sql_results/` | Panel 1 data |
| `dashboard_promo_vs_retention.csv` | `sql_results/` | Panel 2 data |
| `dashboard_geo_opportunity.csv` | `sql_results/` | Panel 3 data |
| `dashboard_category_funnel.csv` | `sql_results/` | Panel 4 data |
| `q4a_segment_profiles.csv` | `sql_results/` | Segment detail |
| `q5a_icp_demographics.csv` | `sql_results/` | ICP metrics |

---

## Dashboard Layout

### Page 1: Founder Overview (4 panels)

**Canvas size**: 1920 × 1080  
**Background**: Dark theme (#0a0e1a)  
**Font**: Segoe UI (Power BI default) or Inter

```
┌──────────────────────────────┬───────────────────────────────┐
│                              │                               │
│   Panel 1: Customer Pyramid  │  Panel 2: Promo vs Loyalty    │
│   (Stacked Bar)              │  (Scatter Plot)               │
│                              │                               │
├──────────────────────────────┼───────────────────────────────┤
│                              │                               │
│   Panel 3: Geographic Map    │  Panel 4: Category Funnel     │
│   (Filled Map + Table)       │  (Stacked Bar Chart)          │
│                              │                               │
└──────────────────────────────┴───────────────────────────────┘
```

---

### Panel 1: Customer Value Pyramid

**Data source**: `dashboard_pyramid.csv`  
**Visual type**: Stacked Bar Chart (horizontal)

| Field | Assignment |
|-------|-----------|
| Y-Axis | `value_tier` (sorted: Platinum → Bronze) |
| X-Axis | `total_revenue` |
| Data Labels | Show `revenue_pct` as percentage |
| Tooltip | `customer_count`, `customer_pct` |

**Formatting**:
- Color by tier: Platinum=#c084fc, Gold=#fbbf24, Silver=#94a3b8, Bronze=#f97316
- Add a Card visual above showing: "Top 25% = 65.1% of revenue"

**DAX Measure** (optional):
```dax
Revenue Share = 
DIVIDE(
    SUM(dashboard_pyramid[total_revenue]),
    CALCULATE(SUM(dashboard_pyramid[total_revenue]), ALL(dashboard_pyramid))
)
```

---

### Panel 2: Promo Dependency vs. Loyalty

**Data source**: `dashboard_promo_vs_retention.csv`  
**Visual type**: Scatter Chart

| Field | Assignment |
|-------|-----------|
| X-Axis | `avg_promo_dependency` |
| Y-Axis | `avg_loyalty` |
| Size | `segment_size` |
| Legend/Color | `customer_segment` |
| Tooltip | `avg_spend`, `promo_usage_pct` |

**Formatting**:
- Segment colors: Champions=#818cf8, At-Risk=#fbbf24, Casual=#94a3b8, Discount=#fb7185, Loyal=#34d399
- Add reference lines at X=0.15 and Y=0.40 to create quadrants
- Enable "Category labels" to show segment names on points

---

### Panel 3: Geographic Opportunity Map

**Data source**: `dashboard_geo_opportunity.csv`  
**Visual type**: Filled Map (US states) OR ArcGIS Map

| Field | Assignment |
|-------|-----------|
| Location | `state` |
| Color saturation | `avg_spend` |
| Tooltip | `customer_count`, `promo_pct`, `avg_promo_dep`, `total_revenue` |

**Formatting**:
- Color scale: Low spend = #1e293b (dark), High spend = #34d399 (emerald)
- Add a secondary Matrix visual below listing top 10 "hidden gem" states (from `q3c_hidden_gems.csv`)

**DAX Measure** (Organic Demand Score):
```dax
Organic Score = 
[avg_spend] * (1 - [promo_pct] / 100)
```

---

### Panel 4: Category Retention Funnel

**Data source**: `dashboard_category_funnel.csv`  
**Visual type**: 100% Stacked Bar Chart (horizontal)

| Field | Assignment |
|-------|-----------|
| Y-Axis | `Category` (sorted by `avg_prev_purchases` ascending) |
| Values | `new_customers`, mid-range (calculated), `veteran_customers` |
| Tooltip | `avg_spend`, `promo_pct`, `avg_loyalty` |

**DAX Measure** (Mid-range customers):
```dax
Mid Customers = [customer_count] - [new_customers] - [veteran_customers]
```

**Formatting**:
- New customers = #fb7185 (rose)
- Mid-range = #334155 (slate)  
- Veterans = #34d399 (emerald)
- Sort categories by `avg_prev_purchases` ascending (entry-point → retention)

---

### Page 2: Segment Deep Dive (optional)

Add a second page with:
- **Segment Slicer**: Filter by `customer_segment`
- **KPI Cards**: customer count, avg spend, loyalty score, promo usage
- **Table**: Full segment profile from `q4a_segment_profiles.csv`
- **Donut Chart**: Revenue concentration by segment

---

## Slicers (All Pages)

| Slicer | Field | Type |
|--------|-------|------|
| Region | `region` | Dropdown |
| Value Tier | `value_tier` | Buttons |
| Category | `Category` | Dropdown |
| Gender | `Gender` | Buttons |

---

## Color Theme

Save as a Power BI theme JSON:

```json
{
  "name": "CustomerIntelligence",
  "dataColors": ["#818cf8", "#34d399", "#fbbf24", "#fb7185", "#94a3b8", "#c084fc", "#22d3ee"],
  "background": "#0a0e1a",
  "foreground": "#f1f5f9",
  "tableAccent": "#818cf8"
}
```

Import via View → Themes → Browse for themes.

---

## Tips

1. **Dark theme**: Use View → Page background → set to #0a0e1a
2. **Font colors**: Set all visual title/label fonts to #f1f5f9 (white)
3. **Borders**: Disable visual borders for a cleaner look
4. **Interactions**: Set scatter chart to cross-filter the other panels
5. **Mobile view**: Create a mobile layout for tablet/phone access
