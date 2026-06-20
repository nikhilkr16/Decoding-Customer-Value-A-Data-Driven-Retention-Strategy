"""
=============================================================================
Customer Value Intelligence — SQL Query Runner
=============================================================================
Loads customer_features.csv into SQLite, executes all segmentation queries,
and exports results as individual CSVs for Power BI / dashboard consumption.
=============================================================================
"""

import sqlite3
import pandas as pd
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

INPUT_FILE = "customer_features.csv"
OUTPUT_DIR = "sql_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1. LOAD DATA INTO SQLITE
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("Loading data into SQLite")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)
print(f"  Loaded {df.shape[0]} rows x {df.shape[1]} columns from {INPUT_FILE}")

conn = sqlite3.connect(":memory:")
df.to_sql("customers", conn, index=False, if_exists="replace")

# Verify load
cursor = conn.execute("SELECT COUNT(*) FROM customers")
count = cursor.fetchone()[0]
print(f"  SQLite table 'customers' created with {count} rows")

# ─────────────────────────────────────────────────────────────────────────────
# 2. DEFINE & EXECUTE QUERIES
# ─────────────────────────────────────────────────────────────────────────────
# SQLite doesn't support PERCENTILE_CONT, so we compute thresholds in Python
# and inject them into queries.

loyalty_q75 = df["loyalty_score"].quantile(0.75)
print(f"\n  Loyalty Q75 threshold: {loyalty_q75:.4f}")

# Define all queries with names
queries = {}

# ── Q1: Value Tier Profiles ──
queries["q1a_value_tier_profiles"] = """
SELECT
    value_tier,
    COUNT(*) AS customer_count,
    ROUND(AVG(Age), 1) AS avg_age,
    ROUND(AVG("Purchase Amount (USD)"), 1) AS avg_purchase_amt,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(SUM(estimated_annual_spend), 0) AS total_revenue,
    ROUND(SUM(estimated_annual_spend) * 100.0 / (SELECT SUM(estimated_annual_spend) FROM customers), 1) AS revenue_pct,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    ROUND(AVG(annual_frequency), 1) AS avg_annual_freq,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(subscription_flag) * 100, 1) AS subscription_pct,
    ROUND(AVG("Review Rating"), 2) AS avg_rating,
    ROUND(AVG(satisfaction_flag) * 100, 1) AS satisfied_pct
FROM customers
GROUP BY value_tier
ORDER BY
    CASE value_tier
        WHEN 'Platinum' THEN 1
        WHEN 'Gold' THEN 2
        WHEN 'Silver' THEN 3
        WHEN 'Bronze' THEN 4
    END
"""

queries["q1b_category_by_tier"] = """
SELECT
    value_tier,
    Category,
    COUNT(*) AS count
FROM customers
GROUP BY value_tier, Category
ORDER BY
    CASE value_tier
        WHEN 'Platinum' THEN 1
        WHEN 'Gold' THEN 2
        WHEN 'Silver' THEN 3
        WHEN 'Bronze' THEN 4
    END,
    count DESC
"""

queries["q1c_payment_by_tier"] = """
SELECT
    value_tier,
    "Payment Method",
    COUNT(*) AS count
FROM customers
GROUP BY value_tier, "Payment Method"
ORDER BY
    CASE value_tier
        WHEN 'Platinum' THEN 1
        WHEN 'Gold' THEN 2
        WHEN 'Silver' THEN 3
        WHEN 'Bronze' THEN 4
    END,
    count DESC
"""

# ── Q2: Category & Season Tenure ──
queries["q2a_category_season_tenure"] = """
SELECT
    Category,
    Season,
    COUNT(*) AS customer_count,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    ROUND(AVG("Review Rating"), 2) AS avg_rating
FROM customers
GROUP BY Category, Season
ORDER BY avg_prev_purchases DESC
"""

queries["q2b_category_entry_vs_retention"] = """
SELECT
    Category,
    COUNT(*) AS total_customers,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    SUM(CASE WHEN "Previous Purchases" <= 10 THEN 1 ELSE 0 END) AS new_customers,
    SUM(CASE WHEN "Previous Purchases" >= 40 THEN 1 ELSE 0 END) AS veteran_customers,
    ROUND(SUM(CASE WHEN "Previous Purchases" <= 10 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS new_customer_pct,
    ROUND(SUM(CASE WHEN "Previous Purchases" >= 40 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS veteran_pct,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty
FROM customers
GROUP BY Category
ORDER BY avg_prev_purchases ASC
"""

queries["q2c_season_tenure"] = """
SELECT
    Season,
    COUNT(*) AS total_customers,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty
FROM customers
GROUP BY Season
ORDER BY avg_prev_purchases ASC
"""

# ── Q3: Geographic Opportunity ──
queries["q3a_state_analysis"] = """
SELECT
    Location AS state,
    region,
    COUNT(*) AS customer_count,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(SUM(estimated_annual_spend), 0) AS total_revenue,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(promo_dependency_score), 4) AS avg_promo_dependency,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    ROUND(AVG("Review Rating"), 2) AS avg_rating,
    ROUND(AVG(estimated_annual_spend) * (1 - AVG(promo_flag)), 0) AS organic_demand_score
FROM customers
GROUP BY Location, region
ORDER BY organic_demand_score DESC
"""

queries["q3b_region_summary"] = """
SELECT
    region,
    COUNT(*) AS customer_count,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(SUM(estimated_annual_spend), 0) AS total_revenue,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(promo_dependency_score), 4) AS avg_promo_dependency,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    ROUND(SUM(CASE WHEN customer_segment = 'Champions' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS champion_pct,
    ROUND(SUM(CASE WHEN customer_segment = 'Discount Hunters' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS discount_hunter_pct
FROM customers
GROUP BY region
ORDER BY avg_annual_spend DESC
"""

queries["q3c_hidden_gems"] = """
SELECT
    Location AS state,
    region,
    COUNT(*) AS customer_count,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(promo_dependency_score), 4) AS avg_promo_dependency
FROM customers
GROUP BY Location, region
HAVING AVG(estimated_annual_spend) > (SELECT AVG(estimated_annual_spend) FROM customers)
   AND AVG(promo_flag) < (SELECT AVG(promo_flag) FROM customers)
ORDER BY avg_annual_spend DESC
"""

# ── Q4: Loyal vs Discount-Only ──
queries["q4a_segment_profiles"] = """
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS pct_of_customers,
    ROUND(SUM(estimated_annual_spend), 0) AS total_revenue,
    ROUND(SUM(estimated_annual_spend) * 100.0 / (SELECT SUM(estimated_annual_spend) FROM customers), 1) AS revenue_pct,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG(Age), 1) AS avg_age,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    ROUND(AVG(annual_frequency), 1) AS avg_annual_freq,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(promo_dependency_score), 4) AS avg_promo_dependency,
    ROUND(AVG(subscription_flag) * 100, 1) AS subscription_pct,
    ROUND(AVG("Review Rating"), 2) AS avg_rating,
    ROUND(AVG(satisfaction_flag) * 100, 1) AS satisfied_pct
FROM customers
GROUP BY customer_segment
ORDER BY avg_annual_spend DESC
"""

queries["q4b_revenue_concentration"] = """
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(SUM(estimated_annual_spend), 0) AS total_revenue,
    ROUND(SUM(estimated_annual_spend) * 100.0 / (SELECT SUM(estimated_annual_spend) FROM customers), 1) AS revenue_pct,
    ROUND(SUM(CASE WHEN promo_flag = 1 THEN estimated_annual_spend ELSE 0 END), 0) AS promo_revenue,
    ROUND(SUM(CASE WHEN promo_flag = 0 THEN estimated_annual_spend ELSE 0 END), 0) AS organic_revenue
FROM customers
GROUP BY customer_segment
ORDER BY total_revenue DESC
"""

queries["q4c_discount_hunter_recovery"] = """
SELECT
    CASE
        WHEN subscription_flag = 1 AND satisfaction_flag = 1 THEN 'Subscribed + Satisfied'
        WHEN subscription_flag = 1 THEN 'Subscribed Only'
        WHEN satisfaction_flag = 1 THEN 'Satisfied Only'
        ELSE 'Neither'
    END AS dh_subgroup,
    COUNT(*) AS count,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_spend,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases
FROM customers
WHERE customer_segment = 'Discount Hunters'
GROUP BY dh_subgroup
ORDER BY avg_spend DESC
"""

queries["q4d_segment_category"] = """
SELECT
    customer_segment,
    Category,
    COUNT(*) AS count,
    ROUND(AVG("Previous Purchases"), 1) AS avg_tenure,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_pct
FROM customers
GROUP BY customer_segment, Category
ORDER BY customer_segment, count DESC
"""

# ── Q5: Ideal Customer Profile ──
queries["q5a_icp_demographics"] = f"""
SELECT
    ROUND(AVG(Age), 1) AS avg_age,
    MIN(Age) AS min_age,
    MAX(Age) AS max_age,
    ROUND(AVG("Purchase Amount (USD)"), 1) AS avg_purchase_amt,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    ROUND(AVG(annual_frequency), 1) AS avg_annual_freq,
    ROUND(AVG("Review Rating"), 2) AS avg_rating,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(subscription_flag) * 100, 1) AS subscription_pct,
    COUNT(*) AS icp_count
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= {loyalty_q75}
"""

queries["q5b_icp_age_gender"] = f"""
SELECT
    age_band,
    Gender,
    COUNT(*) AS count
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= {loyalty_q75}
GROUP BY age_band, Gender
ORDER BY count DESC
"""

queries["q5c_icp_category"] = f"""
SELECT
    Category,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) FROM customers
        WHERE value_tier IN ('Platinum', 'Gold') AND loyalty_score >= {loyalty_q75}
    ), 1) AS pct
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= {loyalty_q75}
GROUP BY Category
ORDER BY count DESC
"""

queries["q5d_icp_payment"] = f"""
SELECT
    "Payment Method",
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) FROM customers
        WHERE value_tier IN ('Platinum', 'Gold') AND loyalty_score >= {loyalty_q75}
    ), 1) AS pct
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= {loyalty_q75}
GROUP BY "Payment Method"
ORDER BY count DESC
"""

queries["q5e_icp_geography"] = f"""
SELECT
    region,
    Location AS state,
    COUNT(*) AS count
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= {loyalty_q75}
GROUP BY region, Location
ORDER BY count DESC
LIMIT 15
"""

# ── Supplementary: Promo Sunset ──
queries["s1_promo_by_segment"] = """
SELECT
    customer_segment,
    COUNT(*) AS total_in_segment,
    SUM(promo_flag) AS promo_users,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(CASE WHEN promo_flag = 1 THEN estimated_annual_spend END), 0) AS avg_spend_promo_users,
    ROUND(AVG(CASE WHEN promo_flag = 0 THEN estimated_annual_spend END), 0) AS avg_spend_non_promo,
    ROUND(AVG(CASE WHEN promo_flag = 1 THEN loyalty_score END), 4) AS avg_loyalty_promo,
    ROUND(AVG(CASE WHEN promo_flag = 0 THEN loyalty_score END), 4) AS avg_loyalty_non_promo
FROM customers
GROUP BY customer_segment
ORDER BY promo_usage_pct DESC
"""

queries["s2_champion_promo_revenue"] = """
SELECT
    customer_segment,
    SUM(CASE WHEN promo_flag = 1 THEN estimated_annual_spend ELSE 0 END) AS promo_revenue,
    SUM(CASE WHEN promo_flag = 0 THEN estimated_annual_spend ELSE 0 END) AS non_promo_revenue,
    ROUND(SUM(CASE WHEN promo_flag = 1 THEN estimated_annual_spend ELSE 0 END) * 100.0
          / SUM(estimated_annual_spend), 1) AS promo_revenue_pct
FROM customers
WHERE customer_segment IN ('Champions', 'Loyal Regulars', 'Casual Browsers')
GROUP BY customer_segment
"""

# ── Dashboard aggregation queries ──
queries["dashboard_pyramid"] = """
SELECT
    value_tier,
    COUNT(*) AS customer_count,
    ROUND(SUM(estimated_annual_spend), 0) AS total_revenue,
    ROUND(SUM(estimated_annual_spend) * 100.0 / (SELECT SUM(estimated_annual_spend) FROM customers), 1) AS revenue_pct,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS customer_pct
FROM customers
GROUP BY value_tier
ORDER BY
    CASE value_tier
        WHEN 'Platinum' THEN 1
        WHEN 'Gold' THEN 2
        WHEN 'Silver' THEN 3
        WHEN 'Bronze' THEN 4
    END
"""

queries["dashboard_promo_vs_retention"] = """
SELECT
    customer_segment,
    ROUND(AVG(promo_dependency_score), 4) AS avg_promo_dependency,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    COUNT(*) AS segment_size,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_spend
FROM customers
GROUP BY customer_segment
"""

queries["dashboard_geo_opportunity"] = """
SELECT
    Location AS state,
    region,
    COUNT(*) AS customer_count,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_pct,
    ROUND(AVG(promo_dependency_score), 4) AS avg_promo_dep,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    ROUND(SUM(estimated_annual_spend), 0) AS total_revenue
FROM customers
GROUP BY Location, region
ORDER BY state
"""

queries["dashboard_category_funnel"] = """
SELECT
    Category,
    COUNT(*) AS customer_count,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_pct,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    SUM(CASE WHEN "Previous Purchases" <= 10 THEN 1 ELSE 0 END) AS new_customers,
    SUM(CASE WHEN "Previous Purchases" >= 40 THEN 1 ELSE 0 END) AS veteran_customers
FROM customers
GROUP BY Category
ORDER BY avg_prev_purchases ASC
"""

# ─────────────────────────────────────────────────────────────────────────────
# 3. EXECUTE ALL QUERIES
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("Executing queries and exporting results")
print("=" * 70)

results_summary = {}

for name, query in queries.items():
    try:
        result_df = pd.read_sql_query(query, conn)
        output_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
        result_df.to_csv(output_path, index=False)
        results_summary[name] = {
            "rows": len(result_df),
            "columns": len(result_df.columns),
            "status": "OK"
        }
        print(f"  [OK] {name}: {len(result_df)} rows x {len(result_df.columns)} cols -> {output_path}")
    except Exception as e:
        results_summary[name] = {
            "rows": 0,
            "columns": 0,
            "status": f"ERROR: {str(e)}"
        }
        print(f"  [ERR] {name}: {str(e)}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. PRINT KEY RESULTS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("KEY RESULTS PREVIEW")
print("=" * 70)

# Value Tier Summary
print("\n--- Q1: Value Tier Profiles ---")
try:
    q1 = pd.read_csv(os.path.join(OUTPUT_DIR, "q1a_value_tier_profiles.csv"))
    print(q1.to_string(index=False))
except:
    print("  Could not load result")

# Segment Profiles
print("\n--- Q4: Customer Segment Profiles ---")
try:
    q4 = pd.read_csv(os.path.join(OUTPUT_DIR, "q4a_segment_profiles.csv"))
    print(q4[["customer_segment", "customer_count", "revenue_pct", "avg_annual_spend",
              "promo_usage_pct", "avg_loyalty"]].to_string(index=False))
except:
    print("  Could not load result")

# ICP
print("\n--- Q5: Ideal Customer Profile ---")
try:
    q5 = pd.read_csv(os.path.join(OUTPUT_DIR, "q5a_icp_demographics.csv"))
    print(q5.T.to_string())
except:
    print("  Could not load result")

# Geographic gems
print("\n--- Q3: Top Hidden Gem States (High Spend + Low Promo) ---")
try:
    q3 = pd.read_csv(os.path.join(OUTPUT_DIR, "q3c_hidden_gems.csv"))
    print(q3.head(10).to_string(index=False))
except:
    print("  Could not load result")

# ─────────────────────────────────────────────────────────────────────────────
# 5. SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
conn.close()

total_ok = sum(1 for v in results_summary.values() if v["status"] == "OK")
total_err = sum(1 for v in results_summary.values() if v["status"] != "OK")
print(f"\n{'=' * 70}")
print(f"COMPLETE: {total_ok} queries succeeded, {total_err} failed")
print(f"Results saved to: {os.path.abspath(OUTPUT_DIR)}/")
print(f"{'=' * 70}")
