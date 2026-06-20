-- =============================================================================
-- Customer Value Intelligence — SQL Segmentation & Analysis
-- =============================================================================
-- D2C Fashion Brand · Retention Strategy Project
-- Database: SQLite (loaded from customer_features.csv)
-- =============================================================================


-- ─────────────────────────────────────────────────────────────────────────────
-- Q1: HIGH-VALUE vs LOW-VALUE — What Separates Them?
-- ─────────────────────────────────────────────────────────────────────────────
-- Purpose: Profile comparison across value tiers to identify what makes
-- Platinum customers different from Bronze customers.
-- ─────────────────────────────────────────────────────────────────────────────

-- Q1a: Value Tier Profile Summary
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
    END;

-- Q1b: Dominant Category by Value Tier
SELECT
    value_tier,
    Category,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY value_tier), 1) AS pct_within_tier
FROM customers
GROUP BY value_tier, Category
ORDER BY
    CASE value_tier
        WHEN 'Platinum' THEN 1
        WHEN 'Gold' THEN 2
        WHEN 'Silver' THEN 3
        WHEN 'Bronze' THEN 4
    END,
    count DESC;

-- Q1c: Payment Method by Value Tier
SELECT
    value_tier,
    "Payment Method",
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY value_tier), 1) AS pct_within_tier
FROM customers
GROUP BY value_tier, "Payment Method"
ORDER BY
    CASE value_tier
        WHEN 'Platinum' THEN 1
        WHEN 'Gold' THEN 2
        WHEN 'Silver' THEN 3
        WHEN 'Bronze' THEN 4
    END,
    count DESC;

-- Q1d: Shipping Preference by Value Tier
SELECT
    value_tier,
    "Shipping Type",
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY value_tier), 1) AS pct_within_tier
FROM customers
GROUP BY value_tier, "Shipping Type"
ORDER BY
    CASE value_tier
        WHEN 'Platinum' THEN 1
        WHEN 'Gold' THEN 2
        WHEN 'Silver' THEN 3
        WHEN 'Bronze' THEN 4
    END,
    count DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Q2: SEASONS & CATEGORIES — Which Associate with Low vs High Tenure?
-- ─────────────────────────────────────────────────────────────────────────────
-- Purpose: Identify entry-point categories (low tenure) vs retention
-- categories (high tenure), and seasonal patterns.
-- ─────────────────────────────────────────────────────────────────────────────

-- Q2a: Category × Season Tenure Analysis
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
ORDER BY avg_prev_purchases DESC;

-- Q2b: Category as Entry-Point vs Retention Indicator
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
ORDER BY avg_prev_purchases ASC;

-- Q2c: Season as Entry-Point vs Retention
SELECT
    Season,
    COUNT(*) AS total_customers,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty
FROM customers
GROUP BY Season
ORDER BY avg_prev_purchases ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Q3: GEOGRAPHY — Organic Demand vs Discount-Driven Volume
-- ─────────────────────────────────────────────────────────────────────────────
-- Purpose: Identify states/regions where the brand has strong organic pull
-- (high spend, low promo dependency) vs discount-dependent markets.
-- ─────────────────────────────────────────────────────────────────────────────

-- Q3a: State-Level Analysis (Top States by Organic Demand Signal)
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
    -- Organic demand signal: high spend + low promo usage
    ROUND(AVG(estimated_annual_spend) * (1 - AVG(promo_flag)), 0) AS organic_demand_score
FROM customers
GROUP BY Location, region
ORDER BY organic_demand_score DESC;

-- Q3b: Region-Level Summary
SELECT
    region,
    COUNT(*) AS customer_count,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(SUM(estimated_annual_spend), 0) AS total_revenue,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(promo_dependency_score), 4) AS avg_promo_dependency,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty,
    -- Segment distribution within region
    ROUND(SUM(CASE WHEN customer_segment = 'Champions' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS champion_pct,
    ROUND(SUM(CASE WHEN customer_segment = 'Discount Hunters' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS discount_hunter_pct
FROM customers
GROUP BY region
ORDER BY avg_annual_spend DESC;

-- Q3c: States with High Spend + Low Promo Dependency (Hidden Gems)
SELECT
    Location AS state,
    region,
    COUNT(*) AS customer_count,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(promo_dependency_score), 4) AS avg_promo_dependency,
    -- Category preference
    (SELECT Category FROM customers c2 WHERE c2.Location = c.Location
     GROUP BY Category ORDER BY COUNT(*) DESC LIMIT 1) AS dominant_category
FROM customers c
GROUP BY Location, region
HAVING AVG(estimated_annual_spend) > (SELECT AVG(estimated_annual_spend) FROM customers)
   AND AVG(promo_flag) < (SELECT AVG(promo_flag) FROM customers)
ORDER BY avg_annual_spend DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Q4: GENUINELY LOYAL vs DISCOUNT-ONLY BUYERS
-- ─────────────────────────────────────────────────────────────────────────────
-- Purpose: Compare Champions vs Discount Hunters head-to-head.
-- Show revenue concentration and promo dependency by segment.
-- ─────────────────────────────────────────────────────────────────────────────

-- Q4a: Full Segment Profile Comparison
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
ORDER BY avg_annual_spend DESC;

-- Q4b: Revenue Concentration — What happens if Discount Hunters leave?
SELECT
    'Total Revenue' AS metric,
    ROUND(SUM(estimated_annual_spend), 0) AS value
FROM customers
UNION ALL
SELECT
    'Revenue from Champions',
    ROUND(SUM(estimated_annual_spend), 0)
FROM customers WHERE customer_segment = 'Champions'
UNION ALL
SELECT
    'Revenue from Discount Hunters',
    ROUND(SUM(estimated_annual_spend), 0)
FROM customers WHERE customer_segment = 'Discount Hunters'
UNION ALL
SELECT
    'Revenue at Risk if DH Leave (%)',
    ROUND(SUM(CASE WHEN customer_segment = 'Discount Hunters' THEN estimated_annual_spend ELSE 0 END)
          * 100.0 / SUM(estimated_annual_spend), 1)
FROM customers;

-- Q4c: Can Discount Hunters survive without promos?
-- Metrics of Discount Hunters who show any loyalty signal
SELECT
    'All Discount Hunters' AS group_label,
    COUNT(*) AS count,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_spend,
    ROUND(AVG(loyalty_score), 4) AS avg_loyalty
FROM customers
WHERE customer_segment = 'Discount Hunters'
UNION ALL
SELECT
    'DH with Subscription',
    COUNT(*),
    ROUND(AVG(estimated_annual_spend), 0),
    ROUND(AVG(loyalty_score), 4)
FROM customers
WHERE customer_segment = 'Discount Hunters' AND subscription_flag = 1
UNION ALL
SELECT
    'DH with High Satisfaction',
    COUNT(*),
    ROUND(AVG(estimated_annual_spend), 0),
    ROUND(AVG(loyalty_score), 4)
FROM customers
WHERE customer_segment = 'Discount Hunters' AND satisfaction_flag = 1;

-- Q4d: Segment × Category — Which categories retain vs churn?
SELECT
    customer_segment,
    Category,
    COUNT(*) AS count,
    ROUND(AVG("Previous Purchases"), 1) AS avg_tenure,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_spend,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_pct
FROM customers
GROUP BY customer_segment, Category
ORDER BY customer_segment,
    CASE Category
        WHEN 'Clothing' THEN 1
        WHEN 'Accessories' THEN 2
        WHEN 'Footwear' THEN 3
        WHEN 'Outerwear' THEN 4
    END;


-- ─────────────────────────────────────────────────────────────────────────────
-- Q5: IDEAL CUSTOMER PROFILE (ICP)
-- ─────────────────────────────────────────────────────────────────────────────
-- Purpose: Build a data-backed description of the brand's most valuable
-- customer, specific enough for marketing targeting.
-- ─────────────────────────────────────────────────────────────────────────────

-- Q5a: ICP Demographics (Platinum + Gold value tier, high loyalty)
SELECT
    'ICP Population' AS metric,
    COUNT(*) AS value
FROM customers
WHERE value_tier IN ('Platinum', 'Gold') AND loyalty_score >= (
    SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers
);

-- Q5b: ICP Demographic Profile
SELECT
    ROUND(AVG(Age), 1) AS avg_age,
    ROUND(MIN(Age), 0) AS min_age,
    ROUND(MAX(Age), 0) AS max_age,
    (SELECT age_band FROM customers
     WHERE value_tier IN ('Platinum', 'Gold')
       AND loyalty_score >= (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers)
     GROUP BY age_band ORDER BY COUNT(*) DESC LIMIT 1) AS modal_age_band,
    (SELECT Gender FROM customers
     WHERE value_tier IN ('Platinum', 'Gold')
       AND loyalty_score >= (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers)
     GROUP BY Gender ORDER BY COUNT(*) DESC LIMIT 1) AS dominant_gender,
    ROUND(AVG("Purchase Amount (USD)"), 1) AS avg_purchase_amt,
    ROUND(AVG(estimated_annual_spend), 0) AS avg_annual_spend,
    ROUND(AVG("Previous Purchases"), 1) AS avg_prev_purchases,
    ROUND(AVG(annual_frequency), 1) AS avg_annual_freq,
    ROUND(AVG("Review Rating"), 2) AS avg_rating,
    ROUND(AVG(promo_flag) * 100, 1) AS promo_usage_pct,
    ROUND(AVG(subscription_flag) * 100, 1) AS subscription_pct
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= (
    SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers
  );

-- Q5c: ICP Category Preference
SELECT
    Category,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) FROM customers
        WHERE value_tier IN ('Platinum', 'Gold')
          AND loyalty_score >= (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers)
    ), 1) AS pct
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= (
    SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers
  )
GROUP BY Category
ORDER BY count DESC;

-- Q5d: ICP Payment & Shipping Preferences
SELECT
    "Payment Method",
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) FROM customers
        WHERE value_tier IN ('Platinum', 'Gold')
          AND loyalty_score >= (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers)
    ), 1) AS pct
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= (
    SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers
  )
GROUP BY "Payment Method"
ORDER BY count DESC;

-- Q5e: ICP Geographic Footprint
SELECT
    region,
    Location AS state,
    COUNT(*) AS count
FROM customers
WHERE value_tier IN ('Platinum', 'Gold')
  AND loyalty_score >= (
    SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loyalty_score) FROM customers
  )
GROUP BY region, Location
ORDER BY count DESC
LIMIT 15;


-- ─────────────────────────────────────────────────────────────────────────────
-- SUPPLEMENTARY: PROMO SUNSET TARGETING
-- ─────────────────────────────────────────────────────────────────────────────
-- Purpose: Identify specific segments for the promo sunset plan.
-- ─────────────────────────────────────────────────────────────────────────────

-- S1: Promo users by segment — who can we safely sunset?
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
ORDER BY promo_usage_pct DESC;

-- S2: Revenue impact if we remove discounts for Champions
SELECT
    customer_segment,
    SUM(CASE WHEN promo_flag = 1 THEN estimated_annual_spend ELSE 0 END) AS promo_revenue,
    SUM(CASE WHEN promo_flag = 0 THEN estimated_annual_spend ELSE 0 END) AS non_promo_revenue,
    ROUND(SUM(CASE WHEN promo_flag = 1 THEN estimated_annual_spend ELSE 0 END) * 100.0
          / SUM(estimated_annual_spend), 1) AS promo_revenue_pct
FROM customers
WHERE customer_segment IN ('Champions', 'Loyal Regulars')
GROUP BY customer_segment;

-- S3: Demographic profile of promo-independent Champions
SELECT
    age_band,
    Gender,
    Category,
    "Payment Method",
    COUNT(*) AS count
FROM customers
WHERE customer_segment = 'Champions' AND promo_flag = 0
GROUP BY age_band, Gender, Category, "Payment Method"
ORDER BY count DESC
LIMIT 20;
