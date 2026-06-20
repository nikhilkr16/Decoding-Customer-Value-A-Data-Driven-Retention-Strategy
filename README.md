<p align="center">
  <img src="https://img.shields.io/badge/SQL-Analysis-0078D4?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" alt="SQL"/>
  <img src="https://img.shields.io/badge/Python-Data%20Prep-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Dashboard-Interactive-FF6F00?style=for-the-badge&logo=googleanalytics&logoColor=white" alt="Dashboard"/>
  <img src="https://img.shields.io/badge/Strategy-Retention-00C853?style=for-the-badge" alt="Retention"/>
</p>

<h1 align="center">Decoding Customer Value<br/><sub>A Data-Driven Retention Strategy</sub></h1>

<p align="center">
  <strong>Nikhil Kumar</strong> · June 2026<br/>
  <em>SQL · Python · Modern Dashboard · Strategic Analytics</em>
</p>

---
<img width="1816" height="875" alt="image" src="https://github.com/user-attachments/assets/45497607-6a4d-47f7-af70-648ecde85a60" />
<img width="1820" height="731" alt="image" src="https://github.com/user-attachments/assets/f8e2010f-29d8-403f-a6de-bc7c623b3d95" />
<img width="1800" height="606" alt="image" src="https://github.com/user-attachments/assets/232c7eb1-fc92-4bb8-b9b0-5b3ed8dd235a" />
<img width="1803" height="647" alt="image" src="https://github.com/user-attachments/assets/b95771c5-4e7a-4439-8263-cdf46e3c25c0" />
<img width="1800" height="606" alt="image" src="https://github.com/user-attachments/assets/73c8d0f6-15b6-4cf1-bdc2-e3c30c219535" />


## 📌 Business Question

> *Is the brand building a loyal customer base, or is it reliant on continuous promotional activity — and what should it do in either scenario?*

## 🔑 One-Line Answer

**The brand has a genuine loyal core, but it is leaking $385K–$552K/yr in margin by discounting customers who would buy anyway.**

---

## 📊 Interactive Dashboard

A custom-built, fully interactive analytics dashboard was designed to communicate findings to non-technical stakeholders.

<img width="1816" alt="Dashboard — Value Pyramid & KPIs" src="https://github.com/user-attachments/assets/45497607-6a4d-47f7-af70-648ecde85a60" />

<details>
<summary><strong>🖼️ View More Dashboard Screenshots</strong></summary>
<br/>

<img width="1820" alt="Promo Dependency Analysis" src="https://github.com/user-attachments/assets/f8e2010f-29d8-403f-a6de-bc7c623b3d95" />

<img width="1800" alt="Category Funnel & Geo Opportunity" src="https://github.com/user-attachments/assets/232c7eb1-fc92-4bb8-b9b0-5b3ed8dd235a" />

<img width="1803" alt="Segment Comparison" src="https://github.com/user-attachments/assets/b95771c5-4e7a-4439-8263-cdf46e3c25c0" />

<img width="1800" alt="Ideal Customer Profile" src="https://github.com/user-attachments/assets/73c8d0f6-15b6-4cf1-bdc2-e3c30c219535" />

</details>

---

## 💡 Key Findings at a Glance

| # | Finding | Business Implication |
|:-:|---------|----------------------|
| 1 | **Top 25% of customers = 65.1% of revenue** | Revenue is heavily concentrated; losing Champions is catastrophic |
| 2 | **43% use promos, but only 11.2% truly depend on them** | ~32% of promo usage is unnecessary margin loss |
| 3 | **Loyalty is driven by frequency, not basket size** ($61.50 vs $59.76 avg) | Marketing should optimize for repeat visits, not order value |
| 4 | **Satisfaction predicts loyalty** (4.11 ICP vs 3.22 At-Risk) | Post-purchase experience is the highest-leverage investment |
| 5 | **13 states show high spend + low promo dependency** | Organic demand exists — ready for amplification |
| 6 | **Subscription rate 1.7× higher among ICPs** (45.6% vs 27%) | Subscription is both a loyalty signal and a loyalty driver |

---

## 🏗️ Methodology & Analysis Pipeline

```
Raw Dataset (3,900 customers)
    │
    ├──▶ Python Data Preparation
    │       • Feature engineering (loyalty score, promo dependency, value tiers)
    │       • Customer segmentation (Champions, Loyal Regulars, At-Risk, etc.)
    │       • Annual spend & frequency estimation
    │
    ├──▶ SQL Deep-Dive Analysis (430+ lines, 15 queries across 5 themes)
    │       • Q1: High-Value vs Low-Value profiling
    │       • Q2: Category & season tenure patterns
    │       • Q3: Geographic organic-demand mapping
    │       • Q4: Loyal vs discount-only buyer comparison
    │       • Q5: Ideal Customer Profile construction
    │
    ├──▶ Interactive HTML/CSS/JS Dashboard
    │       • Value pyramid, KPI cards, segment comparison
    │       • Promo vs retention scatter analysis
    │       • Category funnel & geographic opportunity maps
    │
    └──▶ Strategic Deliverables
            • Executive Summary (1-pager for leadership)
            • Retention Playbook (actionable rollout plans with timelines)
```

---

## 🎯 Customer Segmentation

| Segment | % of Base | % of Revenue | Avg Loyalty Score | Promo Dependency | Action |
|---------|:---------:|:------------:|:-----------------:|:----------------:|--------|
| 🏆 **Champions** | 19.4% | 42.2% | 0.658 | 0.056 (Low) | Sunset promos → loyalty perks |
| ⭐ **Loyal Regulars** | 21.6% | 32.4% | 0.524 | 0.112 | Nurture & upsell subscriptions |
| 👀 **Casual Browsers** | 37.3% | 21.0% | 0.289 | 0.077 | Protect from discount contamination |
| ⚠️ **At-Risk** | 10.5% | — | 0.318 | — | Satisfaction intervention |
| 🏷️ **Discount Hunters** | 11.2% | 4.4% | 0.234 | 0.672 (High) | Phase out / earn-your-discount |

---

## 💰 Recommended Actions & Impact

### 1. Sunset Promos for Champions *(6-month rollout)*
Replace price discounts with loyalty perks (free express shipping, early access).  
**Estimated margin recovery: $375K–$465K/yr**

### 2. Phase Out Discount Hunters
Accept natural attrition of ~216 pure bargain-chasers (2.2% revenue impact). Recover ~220 via "earn your discount" model.  
**Net margin recovery: $10K–$87K/yr**

### 3. Protect Casual Browsers
This segment (37.3% of base) already buys at full price. Do not introduce promos — invest in subscription conversion instead.

<table>
  <tr>
    <td align="center"><h3>$385K–$552K</h3><sub>Estimated Annual Margin Recovery</sub></td>
    <td align="center"><h3>$175K</h3><sub>Maximum Revenue at Risk</sub></td>
    <td align="center"><h3>2.2–3.2×</h3><sub>ROI on Strategy Shift</sub></td>
  </tr>
</table>

---

## 🧬 Ideal Customer Profile (ICP)

> The brand's most valuable customer is **not** defined by age or gender — they are defined by **behavioral consistency**.

| Attribute | ICP | Overall Avg | Delta |
|-----------|:---:|:-----------:|:-----:|
| Purchase Frequency | 37.5×/yr | 17.8×/yr | **+2.1×** |
| Annual Spend | $2,257 | $1,039 | **+2.2×** |
| Satisfaction Rating | 4.11 / 5.0 | 3.75 / 5.0 | **+10%** |
| Subscription Rate | 45.6% | 27.0% | **+1.7×** |
| Promo Dependency | 0.056 | — | **≈ Zero** |

**Strongest acquisition signal:** Customers who buy **2+ times in their first interaction cycle** are the most likely future Champions.

---

## 📁 Repository Structure

```
├── Dataset.csv                    # Raw dataset (3,900 customers)
├── data_preparation.py            # Feature engineering & segmentation
├── customer_features.csv          # Enriched dataset with computed features
├── segmentation_queries.sql       # 430+ lines of analytical SQL
├── run_sql_queries.py             # SQL execution pipeline
├── sql_results/                   # 24 CSV outputs from SQL analysis
├── dashboard/
│   ├── index.html                 # Interactive analytics dashboard
│   ├── style.css                  # Dashboard styling
│   └── dashboard.js               # Dashboard logic & charts
├── executive_summary.md           # 1-page leadership summary
├── retention_playbook.md          # Full tactical playbook with timelines
├── dashboard_design.md            # Design specification
└── powerbi_theme.json             # Brand color theme
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data Preparation | **Python** (Pandas) | Feature engineering, segmentation, data cleaning |
| Analysis | **SQL** (SQLite) | Deep-dive queries, profiling, ICP construction |
| Visualization | **HTML / CSS / JavaScript** | Custom interactive dashboard |
| Strategy | **Markdown** | Executive summary & retention playbook |

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/nikhilkr16/Decoding-Customer-Value-A-Data-Driven-Retention-Strategy.git

# 2. Run data preparation (generates customer_features.csv)
python data_preparation.py

# 3. Run SQL analysis (generates sql_results/)
python run_sql_queries.py

# 4. Open the dashboard
# Simply open dashboard/index.html in any modern browser
```

---

<p align="center">
  <strong>Nikhil Kumar</strong><br/>
  <a href="https://github.com/nikhilkr16">GitHub</a> · 
  <a href="https://www.linkedin.com/in/nikhilkr16/">LinkedIn</a>
</p>
