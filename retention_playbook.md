# Retention Playbook

**Project**: Decoding Customer Value — SQL-Driven Retention Strategy  
**Prepared by**: Nikhil Kumar  
**Date**: June 2026

---

## Part 1: Promotional Sunset Plan

### Context

43% of the brand's 3,900 customers (1,677 customers) currently purchase using discounts or promo codes. However, the brand's promotional program is not uniformly effective. Analysis reveals that promotional spending subsidizes a significant volume of purchases that would likely have occurred without the discount — particularly among high-loyalty, high-frequency customers.

The following plan identifies specific segments where promotional discounts can be gradually reduced, with explicit trade-off analysis for each recommendation.

---

### Sunset Target 1: Champions (Promo-Using Subset)

| Attribute | Detail |
|-----------|--------|
| **Segment** | Champions |
| **Population** | 758 customers (19.4% of base) |
| **Promo users within segment** | 427 customers (56.3%) |
| **Revenue contribution** | 42.2% of total revenue ($1.71M/yr) |
| **Promo revenue** | $919K (53.7% of segment revenue) |
| **Organic revenue** | $792K (46.3% of segment revenue) |
| **Loyalty score** | 0.6575 (highest of all segments) |
| **Promo dependency score** | 0.0564 (lowest — they do NOT depend on promos) |
| **Avg previous purchases** | 33.5 |
| **Satisfaction rate** | 70.8% |

#### Trigger Behavior
- Loyalty score ≥ 0.5214 (top quartile)
- Value tier = Platinum or Gold
- Promo dependency score < 0.10

#### Recommendation
**Gradually reduce discount frequency from every purchase to every 3rd purchase over 6 months, then transition to loyalty-exclusive perks (early access, free shipping upgrades) instead of price discounts.**

#### Rollout Timeline

| Month | Action |
|-------|--------|
| 1–2 | Reduce discount from automatic to opt-in (customer must apply code) |
| 3–4 | Limit promo codes to 1 per 2 purchases; introduce "Champion Perks" (free express shipping, early access to new collections) |
| 5–6 | Remove standard discounts entirely for Champions; maintain loyalty perks only |
| 7+ | Monitor and adjust |

#### Trade-Off

| Gain | Risk |
|------|------|
| **$460K–$550K** estimated annual margin recovery (assuming 50-60% of Champion promo revenue would have been spent at full price, given their near-zero promo dependency) | 5–10% of Champion promo users may reduce purchase frequency temporarily during transition |
| Establishes non-price loyalty levers | Some Champions may feel penalized if peers still receive discounts |
| Protects long-term brand equity | Requires investment in alternative perks program |

#### Success Metric
- **Primary**: Full-price conversion rate among Champions (target: ≥ 75% purchasing without promo within 6 months)
- **Secondary**: Champion segment revenue change (acceptable threshold: no more than -5% decline)
- **Monitor**: Satisfaction score stability (must remain ≥ 4.0)

---

### Sunset Target 2: Casual Browsers (Current Low-Promo Segment)

| Attribute | Detail |
|-----------|--------|
| **Segment** | Casual Browsers |
| **Population** | 1,454 customers (37.3% of base) |
| **Promo users within segment** | 227 customers (15.6%) |
| **Revenue contribution** | 21.0% of total revenue ($849K/yr) |
| **Promo revenue** | $152K (17.9% of segment revenue) |
| **Loyalty score** | 0.2888 |
| **Promo dependency score** | 0.077 |
| **Subscription rate** | 6.7% (lowest) |

#### Trigger Behavior
- Loyalty score < 0.5214
- Promo flag = 0 (already buying without discounts for 84.4%)
- Low subscription rate signals weak brand attachment

#### Recommendation
**Do NOT start offering promos to this segment. They are already buying at full price. Any promotional outreach risks training them to wait for discounts.**

Instead: **Invest in engagement upgrades** — personalized product recommendations, subscription sign-up incentives (non-discount: free shipping, exclusive styles), and satisfaction improvement (their rating is 3.91 vs. Champions' 4.11).

#### Rollout Timeline

| Month | Action |
|-------|--------|
| 1–3 | Launch personalized email campaigns featuring new arrivals (no discount) |
| 3–6 | A/B test subscription offers (free shipping for 3 months vs. 10% first-purchase discount) |
| 6+ | Measure conversion to Loyal Regulars / At-Risk improvement |

#### Trade-Off

| Gain | Risk |
|------|------|
| Protects $697K in organic revenue from discount contamination | Without any incentive, some browsers may churn naturally |
| Low cost — requires marketing effort, not margin sacrifice | Slower conversion to loyalty than discount-driven approaches |

#### Success Metric
- **Primary**: Subscription conversion rate (target: move from 6.7% to 12% within 6 months)
- **Secondary**: Repeat purchase rate increase
- **Monitor**: Churn rate (defined as no purchase in estimated next cycle based on frequency)

---

### Sunset Target 3: Discount Hunters — Strategic Phase-Out

| Attribute | Detail |
|-----------|--------|
| **Segment** | Discount Hunters |
| **Population** | 436 customers (11.2% of base) |
| **Promo users within segment** | 436 customers (100%) |
| **Revenue contribution** | 4.4% of total revenue ($177K/yr) |
| **Promo dependency score** | 0.6723 (highest — heavily dependent) |
| **Loyalty score** | 0.2344 (lowest) |
| **Avg previous purchases** | 12.2 (low tenure) |
| **Subscription rate** | 49.8% |
| **Satisfaction rate** | 22.5% (lowest) |

#### Trigger Behavior
- Promo flag = 1 (always uses discounts)
- Promo dependency score ≥ 0.44 (top tertile among promo users)
- Loyalty score < 0.38 (below median)

#### Sub-Segmentation for Phase-Out

Not all Discount Hunters are equal. Within this segment:

| Sub-group | Count | Action |
|-----------|-------|--------|
| **Subscribed + Satisfied** (showing some loyalty signals) | ~50 customers | Transition to non-discount perks; potential recovery |
| **Subscribed Only** (committed but not happy) | ~170 customers | Investigate satisfaction gap; may recover with product/service improvements |
| **Neither** (pure bargain chasers) | ~216 customers | Accept natural attrition; stop discounting |

#### Recommendation
**Accept that ~50% of Discount Hunters (216 customers) will churn when discounts are removed. This is strategically acceptable — they contribute only $177K total (4.4% of revenue) while consuming margin on every transaction.**

For the recoverable sub-group (~220 with subscription signals): transition to conditional discounts — require 2 full-price purchases before earning a discount on the 3rd.

#### Rollout Timeline

| Month | Action |
|-------|--------|
| 1–2 | Identify the ~220 "recoverable" DHs with subscription signals |
| 3–4 | For recoverables: shift to "earn your discount" (2 full-price → 1 discounted) |
| 5–6 | For pure bargain chasers: remove proactive promo outreach; allow natural attrition |
| 7+ | Re-segment survivors into At-Risk or Casual Browsers |

#### Trade-Off

| Gain | Risk |
|------|------|
| **$100K–$177K** in margin recovery (discounts were funding nearly all DH revenue) | Lose up to 216 customers (5.5% of base) |
| Cleaner customer base with higher average value | Short-term revenue dip of ~$90K (2.2% of total) |
| Marketing budget freed for Champions and At-Risk | Some negative word-of-mouth from departing customers |

#### Success Metric
- **Primary**: Net revenue impact after 6 months (acceptable: max -2.5% overall decline)
- **Secondary**: Recoverable DH conversion rate (target: 30% make at least 2 full-price purchases)
- **Monitor**: Overall customer count trajectory

---

### Summary: Total Margin Recovery Potential

| Target | Est. Margin Recovery | Revenue at Risk | Net Impact |
|--------|---------------------|-----------------|------------|
| Champions (sunset promos) | $460K–$550K | -$85K (5% of segment) | **+$375K–$465K** |
| Casual Browsers (protect full-price) | $0 (protection play) | $0 | **Protected $697K** |
| Discount Hunters (phase out) | $100K–$177K | -$90K | **+$10K–$87K** |
| **Total** | **$560K–$727K** | **-$175K** | **+$385K–$552K** |

---

## Part 2: Ideal Customer Profile (ICP)

### Data-Backed Definition

The ICP is derived from customers in the **Platinum or Gold value tier** with a **loyalty score ≥ 0.5214** (top quartile). This population represents **758 customers (19.4% of the base)** generating **42.2% of total revenue**.

### The Profile

| Attribute | ICP Value | Overall Average | Delta |
|-----------|-----------|-----------------|-------|
| **Age** | 44.7 years (range: 18–70) | 44.1 years | Similar; age is not a differentiator |
| **Dominant age group** | 46–55 | 26–35 | ICP skews slightly older |
| **Gender** | 76% Male / 24% Female | 68% Male / 32% Female | Slightly more male |
| **Purchase frequency** | 37.5×/year (weekly–fortnightly) | 17.8×/year | **2.1× more frequent** |
| **Avg order value** | $61.50 | $59.76 | Similar; frequency drives value, not order size |
| **Est. annual spend** | $2,257 | $1,039 | **2.2× higher** |
| **Previous purchases** | 33.5 | 25.4 | **32% more purchase history** |
| **Review rating** | 4.11 / 5.0 | 3.75 / 5.0 | **10% higher satisfaction** |
| **Satisfaction rate** | 70.8% | 41.9% | **1.7× more likely to be satisfied** |
| **Subscription rate** | 45.6% | 27.0% | **1.7× more likely to subscribe** |
| **Promo usage** | 56.3% | 43.0% | Uses promos but NOT dependent (dep. score: 0.056) |
| **Top category** | Clothing (45%) | Clothing (44.5%) | Aligned with overall mix |
| **Payment preference** | Credit Card | Credit Card | Aligned |

### Key Insight

**The ICP is not defined by demographics or category — it is defined by behavior.**

The single strongest differentiator is **purchase frequency**: ICPs buy 2.1× more often than average. They are not spending dramatically more per order ($61.50 vs $59.76) — they are simply buying more consistently.

The second differentiator is **satisfaction**: 70.8% of ICPs rate ≥ 4.0, compared to 41.9% overall. Satisfied customers buy more often. This creates a virtuous cycle.

The third differentiator is **subscription commitment**: 45.6% are subscribed versus 27% overall. Subscription is both a signal of and contributor to loyalty.

### Targeting Guidance for Marketing

To acquire more customers who look like the ICP:

1. **Target by behavior, not demographics**: Age and gender are poor predictors. Instead, target lookalike audiences based on purchase frequency signals (e.g., customers who made 2+ purchases in their first 60 days)

2. **Emphasize subscription at onboarding**: The 45.6% subscription rate among ICPs vs. 6.7% among Casual Browsers suggests subscription is a powerful lever. Offer subscription as a default option during checkout with a non-discount perk (free shipping, early access)

3. **Invest in satisfaction improvement**: The causal chain appears to be: satisfaction → frequency → value. Focus on post-purchase experience (shipping speed, product quality feedback loops, easy returns) to drive satisfaction above 4.0

4. **Do not lead with discounts for acquisition**: The ICP's promo dependency score is 0.056 — nearly zero. Discount-led acquisition attracts Discount Hunters (dep. score: 0.672), not future Champions

5. **Geographic focus**: Concentrate paid acquisition in the 13 "hidden gem" states (Illinois, Alaska, Tennessee, Louisiana, Georgia, New York, Alabama, Wyoming, Arizona, Virginia, Rhode Island, Nebraska, Texas) where the brand already has above-average spend with below-average promo dependency — this is organic demand waiting to be amplified

---

*This playbook is designed to be actionable today. Every recommendation names the segment, the trigger behavior, the timeline, the trade-off, and the metric. Assertions are traceable to the underlying data.*
