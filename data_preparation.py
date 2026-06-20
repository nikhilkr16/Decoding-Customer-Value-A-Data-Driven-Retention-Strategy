"""
=============================================================================
Customer Value Intelligence — Data Preparation & Feature Engineering
=============================================================================
D2C Fashion Brand · Retention Strategy Project

This script:
  1. Loads and cleans the raw dataset
  2. Engineers customer-level behavioral metrics
  3. Builds two competing loyalty definitions and selects a winner
  4. Assigns traceable customer segments
  5. Exports cleaned_dataset.csv and customer_features.csv
=============================================================================
"""

import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
INPUT_FILE = "Dataset.csv"
OUTPUT_CLEANED = "cleaned_dataset.csv"
OUTPUT_FEATURES = "customer_features.csv"
OUTPUT_LOYALTY = "loyalty_comparison.csv"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# ─────────────────────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("STEP 1: Loading raw dataset")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)
print(f"  Loaded {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  Columns: {list(df.columns)}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. DATA CLEANING
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 2: Cleaning data")
print("=" * 70)

# 2a. Check Discount / Promo alignment
promo_match = (df["Discount Applied"] == df["Promo Code Used"]).all()
print(f"\n  Discount Applied == Promo Code Used for all rows? {promo_match}")
if promo_match:
    print("  → Consolidating into single 'promo_flag' column")
    df["promo_flag"] = (df["Discount Applied"] == "Yes").astype(int)
else:
    # If not identical, create separate flags
    df["promo_flag"] = (
        (df["Discount Applied"] == "Yes") | (df["Promo Code Used"] == "Yes")
    ).astype(int)
    print("  → Created 'promo_flag' (1 if either discount or promo used)")

# 2b. Handle missing Review Rating — impute with median by Category
null_count = df["Review Rating"].isnull().sum()
print(f"\n  Missing Review Ratings: {null_count}")
if null_count > 0:
    category_medians = df.groupby("Category")["Review Rating"].median()
    print("  Category-level medians for imputation:")
    for cat, med in category_medians.items():
        print(f"    {cat}: {med}")
    df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(
        lambda x: x.fillna(x.median())
    )
    remaining_nulls = df["Review Rating"].isnull().sum()
    print(f"  → After imputation: {remaining_nulls} nulls remaining")

# 2c. Standardize Frequency of Purchases → numeric annual frequency
frequency_map = {
    "Weekly": 52,
    "Fortnightly": 26,
    "Bi-Weekly": 26,
    "Monthly": 12,
    "Every 3 Months": 4,
    "Quarterly": 4,
    "Annually": 1,
}
print(f"\n  Mapping 'Frequency of Purchases' to annual frequency:")
for label, freq in sorted(frequency_map.items(), key=lambda x: -x[1]):
    print(f"    {label:>20s} → {freq} times/year")

df["annual_frequency"] = df["Frequency of Purchases"].map(frequency_map)
unmapped = df["annual_frequency"].isnull().sum()
if unmapped > 0:
    print(f"  ⚠ {unmapped} rows with unmapped frequency values!")
    print(f"    Values: {df.loc[df['annual_frequency'].isnull(), 'Frequency of Purchases'].unique()}")
else:
    print(f"  → All {df.shape[0]} rows mapped successfully")

# 2d. Binary encoding of Subscription Status
df["subscription_flag"] = (df["Subscription Status"] == "Yes").astype(int)

# 2e. Export cleaned dataset
df_cleaned = df.copy()
df_cleaned.to_csv(OUTPUT_CLEANED, index=False)
print(f"\n  ✓ Cleaned dataset saved to '{OUTPUT_CLEANED}' ({df_cleaned.shape[0]} rows)")

# ─────────────────────────────────────────────────────────────────────────────
# 3. FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 3: Engineering customer-level features")
print("=" * 70)

# ── 3a. VALUE METRICS ──
print("\n  [A] Value Metrics")

# Estimated Annual Spend — the closest proxy to CLV we can build
df["estimated_annual_spend"] = df["Purchase Amount (USD)"] * df["annual_frequency"]
print(f"    estimated_annual_spend: min=${df['estimated_annual_spend'].min()}, "
      f"max=${df['estimated_annual_spend'].max()}, "
      f"mean=${df['estimated_annual_spend'].mean():.0f}, "
      f"median=${df['estimated_annual_spend'].median():.0f}")

# Value Tier — quartile-based
df["value_tier"] = pd.qcut(
    df["estimated_annual_spend"],
    q=4,
    labels=["Bronze", "Silver", "Gold", "Platinum"],
)
tier_counts = df["value_tier"].value_counts().sort_index()
print(f"    Value tier distribution:")
for tier, count in tier_counts.items():
    tier_revenue = df.loc[df["value_tier"] == tier, "estimated_annual_spend"].sum()
    total_revenue = df["estimated_annual_spend"].sum()
    pct = tier_revenue / total_revenue * 100
    print(f"      {tier:>10s}: {count:>5d} customers ({pct:.1f}% of total revenue)")

# Spend Rank Percentile — continuous version
df["spend_rank_pctile"] = df["estimated_annual_spend"].rank(pct=True)

# ── 3b. LOYALTY / ENGAGEMENT METRICS ──
print("\n  [B] Loyalty / Engagement Metrics")

# Purchase Frequency Score (0–1 normalized)
df["purchase_frequency_score"] = (
    (df["annual_frequency"] - df["annual_frequency"].min())
    / (df["annual_frequency"].max() - df["annual_frequency"].min())
)
print(f"    purchase_frequency_score: min={df['purchase_frequency_score'].min():.3f}, "
      f"max={df['purchase_frequency_score'].max():.3f}")

# Tenure Proxy — Previous Purchases (directly used, also normalized)
df["tenure_proxy"] = df["Previous Purchases"]
df["tenure_proxy_norm"] = (
    (df["tenure_proxy"] - df["tenure_proxy"].min())
    / (df["tenure_proxy"].max() - df["tenure_proxy"].min())
)
print(f"    tenure_proxy: min={df['tenure_proxy'].min()}, max={df['tenure_proxy'].max()}")

# Satisfaction Flag — binary at 4.0 threshold
df["satisfaction_flag"] = (df["Review Rating"] >= 4.0).astype(int)
sat_pct = df["satisfaction_flag"].mean() * 100
print(f"    satisfaction_flag: {sat_pct:.1f}% of customers are 'satisfied' (rating ≥ 4.0)")

# ── 3c. PROMOTIONAL DEPENDENCY METRICS ──
print("\n  [C] Promotional Dependency Metrics")

# Promo Dependency Score — composite metric
# Logic: A customer who uses promos AND buys infrequently AND has low tenure
# is most likely discount-dependent. High score = more dependent.
df["promo_dependency_score"] = (
    df["promo_flag"]
    * (1 - df["purchase_frequency_score"])
    * (1 - df["tenure_proxy_norm"])
)
# Normalize to 0-1 range
pds_max = df["promo_dependency_score"].max()
if pds_max > 0:
    df["promo_dependency_score"] = df["promo_dependency_score"] / pds_max

promo_users = df["promo_flag"].sum()
print(f"    promo_flag: {promo_users} customers ({promo_users/len(df)*100:.1f}%) used promos")
print(f"    promo_dependency_score: mean={df['promo_dependency_score'].mean():.3f}, "
      f"median={df['promo_dependency_score'].median():.3f}")

# Promo Sensitivity Group — tertile-based
# Only among promo users; non-promo users get "None"
df["promo_sensitivity_group"] = "None"
promo_mask = df["promo_flag"] == 1
if promo_mask.sum() > 0:
    df.loc[promo_mask, "promo_sensitivity_group"] = pd.qcut(
        df.loc[promo_mask, "promo_dependency_score"],
        q=3,
        labels=["Low", "Medium", "High"],
        duplicates="drop",
    )
print(f"    promo_sensitivity_group distribution:")
for group, count in df["promo_sensitivity_group"].value_counts().sort_index().items():
    print(f"      {group:>8s}: {count}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. COMPETING LOYALTY DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 4: Building & comparing two loyalty definitions")
print("=" * 70)

# ── Definition A: Behavior-Weighted Loyalty ──
# Weights tenure and frequency most heavily.
# Rationale: Loyalty is about repeated, consistent purchasing over time.
df["loyalty_A"] = (
    0.35 * df["tenure_proxy_norm"]
    + 0.30 * df["purchase_frequency_score"]
    + 0.20 * df["satisfaction_flag"]
    + 0.15 * df["subscription_flag"]
)

# ── Definition B: Value-Adjusted Loyalty ──
# Adds promo independence as a loyalty signal.
# Rationale: A truly loyal customer buys without needing discounts.
df["loyalty_B"] = (
    0.25 * df["tenure_proxy_norm"]
    + 0.25 * df["purchase_frequency_score"]
    + 0.25 * (1 - df["promo_flag"])
    + 0.15 * df["satisfaction_flag"]
    + 0.10 * df["subscription_flag"]
)

print("\n  Definition A (Behavior-Weighted):")
print(f"    Formula: 0.35×tenure + 0.30×frequency + 0.20×satisfaction + 0.15×subscription")
print(f"    Mean: {df['loyalty_A'].mean():.4f}  |  Std: {df['loyalty_A'].std():.4f}")
print(f"    Range: [{df['loyalty_A'].min():.4f}, {df['loyalty_A'].max():.4f}]")

print("\n  Definition B (Value-Adjusted, includes promo independence):")
print(f"    Formula: 0.25×tenure + 0.25×frequency + 0.25×(1-promo) + 0.15×satisfaction + 0.10×subscription")
print(f"    Mean: {df['loyalty_B'].mean():.4f}  |  Std: {df['loyalty_B'].std():.4f}")
print(f"    Range: [{df['loyalty_B'].min():.4f}, {df['loyalty_B'].max():.4f}]")

# ── Validation Test 1: Correlation with Estimated Annual Spend ──
corr_A = df["loyalty_A"].corr(df["estimated_annual_spend"])
corr_B = df["loyalty_B"].corr(df["estimated_annual_spend"])
print(f"\n  Validation Test 1 — Correlation with estimated_annual_spend:")
print(f"    Loyalty A ↔ Spend: r = {corr_A:.4f}")
print(f"    Loyalty B ↔ Spend: r = {corr_B:.4f}")

# ── Validation Test 2: Separation Power ──
# Does the loyalty score separate top-25% spenders from bottom-25%?
top_spenders = df["estimated_annual_spend"] >= df["estimated_annual_spend"].quantile(0.75)
bot_spenders = df["estimated_annual_spend"] <= df["estimated_annual_spend"].quantile(0.25)

sep_A = df.loc[top_spenders, "loyalty_A"].mean() - df.loc[bot_spenders, "loyalty_A"].mean()
sep_B = df.loc[top_spenders, "loyalty_B"].mean() - df.loc[bot_spenders, "loyalty_B"].mean()
print(f"\n  Validation Test 2 — Separation (Top 25% mean - Bottom 25% mean):")
print(f"    Loyalty A gap: {sep_A:.4f}")
print(f"    Loyalty B gap: {sep_B:.4f}")

# ── Validation Test 3: Internal Consistency ──
# Among high-loyalty customers (top quartile), what % are promo-independent?
loyalty_A_high = df["loyalty_A"] >= df["loyalty_A"].quantile(0.75)
loyalty_B_high = df["loyalty_B"] >= df["loyalty_B"].quantile(0.75)

promo_indep_A = 1 - df.loc[loyalty_A_high, "promo_flag"].mean()
promo_indep_B = 1 - df.loc[loyalty_B_high, "promo_flag"].mean()
print(f"\n  Validation Test 3 — Promo independence among top-25% loyal:")
print(f"    Loyalty A: {promo_indep_A:.1%} are promo-independent")
print(f"    Loyalty B: {promo_indep_B:.1%} are promo-independent")

# ── WINNER SELECTION ──
# Score each definition on the three tests
scores = {"A": 0, "B": 0}
# Test 1: Higher absolute correlation = better
if abs(corr_A) > abs(corr_B):
    scores["A"] += 1
else:
    scores["B"] += 1
# Test 2: Larger separation = better
if abs(sep_A) > abs(sep_B):
    scores["A"] += 1
else:
    scores["B"] += 1
# Test 3: Higher promo independence = more internally consistent
if promo_indep_A > promo_indep_B:
    scores["A"] += 1
else:
    scores["B"] += 1

winner = "A" if scores["A"] > scores["B"] else "B"
print(f"\n  ┌─────────────────────────────────────────────────────────┐")
print(f"  │  WINNER: Definition {winner} (Score: A={scores['A']}, B={scores['B']})           │")
print(f"  └─────────────────────────────────────────────────────────┘")

# Use winning definition as the primary loyalty score
df["loyalty_score"] = df[f"loyalty_{winner}"]
winning_label = "Behavior-Weighted" if winner == "A" else "Value-Adjusted"
print(f"\n  Using '{winning_label}' as primary loyalty_score for segmentation")

# Export loyalty comparison
loyalty_export = df[
    ["Customer ID", "loyalty_A", "loyalty_B", "loyalty_score",
     "estimated_annual_spend", "promo_flag", "tenure_proxy_norm",
     "purchase_frequency_score", "satisfaction_flag", "subscription_flag"]
].copy()
loyalty_export.to_csv(OUTPUT_LOYALTY, index=False)
print(f"\n  ✓ Loyalty comparison saved to '{OUTPUT_LOYALTY}'")

# ─────────────────────────────────────────────────────────────────────────────
# 5. CUSTOMER SEGMENTATION
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 5: Assigning traceable customer segments")
print("=" * 70)

# Segment assignment rules (every label maps to explicit variable combinations):
#
# Champions:       High loyalty (≥75th pctile) AND Platinum/Gold value tier
# Loyal Regulars:  High loyalty (≥75th pctile) AND Silver/Bronze value tier
# Discount Hunters: High promo dependency (≥66th pctile among promo users)
#                   AND Low loyalty (<50th pctile)
# At-Risk:          Medium loyalty (25th–75th pctile) AND satisfaction_flag=0
# Casual Browsers:  Everything else (low loyalty, low value, no strong signals)

loyalty_q75 = df["loyalty_score"].quantile(0.75)
loyalty_q50 = df["loyalty_score"].quantile(0.50)
loyalty_q25 = df["loyalty_score"].quantile(0.25)

# Promo dependency threshold for "high dependency"
promo_dep_q66 = df.loc[df["promo_flag"] == 1, "promo_dependency_score"].quantile(0.66)

def assign_segment(row):
    """Assign customer segment based on traceable variable combinations."""
    loyalty = row["loyalty_score"]
    value = row["value_tier"]
    promo_dep = row["promo_dependency_score"]
    promo = row["promo_flag"]
    satisfied = row["satisfaction_flag"]

    # Champions: high loyalty + high value
    if loyalty >= loyalty_q75 and value in ["Platinum", "Gold"]:
        return "Champions"

    # Loyal Regulars: high loyalty + lower value
    if loyalty >= loyalty_q75 and value in ["Silver", "Bronze"]:
        return "Loyal Regulars"

    # Discount Hunters: high promo dependency + low loyalty
    if promo == 1 and promo_dep >= promo_dep_q66 and loyalty < loyalty_q50:
        return "Discount Hunters"

    # At-Risk: mid loyalty + not satisfied
    if loyalty_q25 <= loyalty < loyalty_q75 and satisfied == 0:
        return "At-Risk"

    # Casual Browsers: everything else
    return "Casual Browsers"


df["customer_segment"] = df.apply(assign_segment, axis=1)

print("\n  Segment Thresholds:")
print(f"    Loyalty Q75 (Champion/Loyal threshold): {loyalty_q75:.4f}")
print(f"    Loyalty Q50 (Discount Hunter ceiling):  {loyalty_q50:.4f}")
print(f"    Loyalty Q25 (At-Risk floor):            {loyalty_q25:.4f}")
print(f"    Promo Dep Q66 (High dependency):        {promo_dep_q66:.4f}")

print("\n  Segment Distribution:")
seg_stats = df.groupby("customer_segment").agg(
    count=("Customer ID", "count"),
    avg_spend=("estimated_annual_spend", "mean"),
    total_revenue=("estimated_annual_spend", "sum"),
    avg_loyalty=("loyalty_score", "mean"),
    promo_rate=("promo_flag", "mean"),
    avg_satisfaction=("Review Rating", "mean"),
).sort_values("avg_spend", ascending=False)

total_rev = df["estimated_annual_spend"].sum()
for seg, row in seg_stats.iterrows():
    rev_pct = row["total_revenue"] / total_rev * 100
    print(f"    {seg:>18s}: {row['count']:>5.0f} customers | "
          f"Avg Spend: ${row['avg_spend']:>7,.0f} | "
          f"Revenue: {rev_pct:>5.1f}% | "
          f"Promo Rate: {row['promo_rate']:.0%} | "
          f"Avg Rating: {row['avg_satisfaction']:.1f}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. ADDITIONAL DERIVED FEATURES FOR DASHBOARD / SQL
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 6: Additional derived features")
print("=" * 70)

# Age Band — for demographic profiling
bins = [17, 25, 35, 45, 55, 65, 71]
labels = ["18-25", "26-35", "36-45", "46-55", "56-65", "66-70"]
df["age_band"] = pd.cut(df["Age"], bins=bins, labels=labels)
print(f"\n  Age band distribution:")
for band, count in df["age_band"].value_counts().sort_index().items():
    print(f"    {band}: {count}")

# Region mapping (US Census regions)
region_map = {
    # Northeast
    "Connecticut": "Northeast", "Maine": "Northeast", "Massachusetts": "Northeast",
    "New Hampshire": "Northeast", "Rhode Island": "Northeast", "Vermont": "Northeast",
    "New Jersey": "Northeast", "New York": "Northeast", "Pennsylvania": "Northeast",
    # Midwest
    "Illinois": "Midwest", "Indiana": "Midwest", "Michigan": "Midwest",
    "Ohio": "Midwest", "Wisconsin": "Midwest", "Iowa": "Midwest",
    "Kansas": "Midwest", "Minnesota": "Midwest", "Missouri": "Midwest",
    "Nebraska": "Midwest", "North Dakota": "Midwest", "South Dakota": "Midwest",
    # South
    "Delaware": "South", "Florida": "South", "Georgia": "South",
    "Maryland": "South", "North Carolina": "South", "South Carolina": "South",
    "Virginia": "South", "West Virginia": "South", "Alabama": "South",
    "Kentucky": "South", "Mississippi": "South", "Tennessee": "South",
    "Arkansas": "South", "Louisiana": "South", "Oklahoma": "South",
    "Texas": "South",
    # West
    "Arizona": "West", "Colorado": "West", "Idaho": "West",
    "Montana": "West", "Nevada": "West", "New Mexico": "West",
    "Utah": "West", "Wyoming": "West", "Alaska": "West",
    "California": "West", "Hawaii": "West", "Oregon": "West",
    "Washington": "West",
    # DC
    "District of Columbia": "South",
}
df["region"] = df["Location"].map(region_map)
unmapped_regions = df["region"].isnull().sum()
if unmapped_regions > 0:
    print(f"\n  ⚠ {unmapped_regions} states not mapped to regions")
    print(f"    {df.loc[df['region'].isnull(), 'Location'].unique()}")
else:
    print(f"\n  Region distribution:")
    for region, count in df["region"].value_counts().sort_index().items():
        print(f"    {region}: {count}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. EXPORT FINAL FEATURE TABLE
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 7: Exporting final customer features table")
print("=" * 70)

feature_cols = [
    "Customer ID", "Age", "age_band", "Gender", "Location", "region",
    "Item Purchased", "Category", "Size", "Color", "Season",
    "Purchase Amount (USD)", "annual_frequency", "Frequency of Purchases",
    "Previous Purchases", "Review Rating",
    "Subscription Status", "subscription_flag",
    "Shipping Type", "Payment Method",
    "Discount Applied", "Promo Code Used", "promo_flag",
    # Engineered features
    "estimated_annual_spend", "value_tier", "spend_rank_pctile",
    "purchase_frequency_score", "tenure_proxy", "tenure_proxy_norm",
    "satisfaction_flag",
    "promo_dependency_score", "promo_sensitivity_group",
    "loyalty_A", "loyalty_B", "loyalty_score",
    "customer_segment",
]

df_features = df[feature_cols].copy()
df_features.to_csv(OUTPUT_FEATURES, index=False)
print(f"\n  ✓ Customer features saved to '{OUTPUT_FEATURES}'")
print(f"    {df_features.shape[0]} customers × {df_features.shape[1]} features")

# ─────────────────────────────────────────────────────────────────────────────
# 8. SUMMARY STATISTICS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  Dataset:           {df.shape[0]} customers
  Value Tiers:       {df['value_tier'].nunique()} (Bronze → Platinum)
  Customer Segments: {df['customer_segment'].nunique()}
  Loyalty Winner:    Definition {winner} ({winning_label})
  Total Est. Revenue: ${total_rev:,.0f}
  Promo Users:       {promo_users} ({promo_users/len(df)*100:.1f}%)
  Subscribers:       {df['subscription_flag'].sum()} ({df['subscription_flag'].mean()*100:.1f}%)
  Avg Satisfaction:  {df['Review Rating'].mean():.2f} / 5.0

  Output Files:
    → {OUTPUT_CLEANED}
    → {OUTPUT_FEATURES}
    → {OUTPUT_LOYALTY}
""")

print("✓ Data preparation complete!")
