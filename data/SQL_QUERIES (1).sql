
-- 1. COHORT RETENTION ANALYSIS


-- Calculate retention rate by cohort and months since registration
WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', registration_date) AS cohort_month,
        registration_date
    FROM customers
),
order_months AS (
    SELECT 
        o.customer_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) AS order_month,
        EXTRACT(MONTH FROM AGE(o.order_date, c.registration_date)) AS months_since_registration,
        SUM(o.revenue) AS revenue
    FROM orders o
    JOIN customer_cohorts c ON o.customer_id = c.customer_id
    GROUP BY 1, 2, 3, 4
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_cohorts
    GROUP BY 1
)
SELECT 
    cs.cohort_month,
    om.months_since_registration,
    cs.cohort_size,
    COUNT(DISTINCT om.customer_id) AS active_customers,
    ROUND(COUNT(DISTINCT om.customer_id)::NUMERIC / cs.cohort_size * 100, 2) AS retention_rate,
    ROUND(SUM(om.revenue), 2) AS cohort_revenue,
    ROUND(SUM(om.revenue) / cs.cohort_size, 2) AS revenue_per_customer
FROM cohort_sizes cs
LEFT JOIN order_months om ON cs.cohort_month = om.cohort_month
GROUP BY 1, 2, 3
ORDER BY 1, 2;


-- 2. CUSTOMER LIFETIME VALUE (LTV) AND UNIT ECONOMICS


WITH customer_revenue AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS num_orders,
        MIN(order_date) AS first_order,
        MAX(order_date) AS last_order,
        SUM(revenue) AS total_revenue,
        SUM(cogs) AS total_cogs,
        SUM(gross_profit) AS total_profit
    FROM orders
    GROUP BY customer_id
),
marketing_cac AS (
    SELECT 
        channel,
        AVG(cac) AS avg_cac
    FROM marketing_costs
    GROUP BY channel
)
SELECT 
    c.customer_id,
    c.registration_date,
    c.channel,
    c.customer_segment,
    COALESCE(cr.num_orders, 0) AS num_orders,
    cr.first_order,
    cr.last_order,
    COALESCE(cr.total_revenue, 0) AS ltv,
    COALESCE(cr.total_cogs, 0) AS total_cogs,
    COALESCE(cr.total_profit, 0) AS total_profit,
    mc.avg_cac AS cac,
    -- Unit Economics: Profit per Customer = LTV - CAC - COGS
    COALESCE(cr.total_revenue, 0) - mc.avg_cac - COALESCE(cr.total_cogs, 0) AS unit_economics,
    -- LTV/CAC Ratio
    CASE 
        WHEN mc.avg_cac > 0 THEN ROUND(COALESCE(cr.total_revenue, 0) / mc.avg_cac, 2)
        ELSE 0 
    END AS ltv_cac_ratio,
    -- Time to First Value (days from registration to first order)
    EXTRACT(DAY FROM AGE(cr.first_order, c.registration_date)) AS time_to_first_value,
    -- Activation flag
    CASE WHEN cr.num_orders > 0 THEN 1 ELSE 0 END AS is_activated,
    -- Customer lifespan
    EXTRACT(DAY FROM AGE(cr.last_order, cr.first_order)) AS customer_lifespan_days
FROM customers c
LEFT JOIN customer_revenue cr ON c.customer_id = cr.customer_id
LEFT JOIN marketing_cac mc ON c.channel = mc.channel;

-- 3. MONTHLY KPIs (Revenue, ARPU, CAC, Gross Margin)

WITH monthly_revenue AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        SUM(revenue) AS revenue,
        SUM(cogs) AS cogs,
        SUM(gross_profit) AS gross_profit,
        COUNT(DISTINCT customer_id) AS active_customers,
        COUNT(DISTINCT order_id) AS num_orders
    FROM orders
    GROUP BY 1
),
monthly_new_customers AS (
    SELECT 
        DATE_TRUNC('month', registration_date) AS month,
        COUNT(DISTINCT customer_id) AS new_customers
    FROM customers
    GROUP BY 1
),
monthly_marketing AS (
    SELECT 
        month,
        SUM(ad_spend) AS ad_spend
    FROM marketing_costs
    GROUP BY 1
)
SELECT 
    mr.month,
    mr.revenue,
    mr.cogs,
    mr.gross_profit,
    ROUND((mr.gross_profit / NULLIF(mr.revenue, 0)) * 100, 2) AS gross_margin,
    mr.active_customers,
    mr.num_orders,
    nc.new_customers,
    mm.ad_spend,
    -- ARPU (Average Revenue Per User)
    ROUND(mr.revenue / NULLIF(mr.active_customers, 0), 2) AS arpu,
    -- Average Order Value
    ROUND(mr.revenue / NULLIF(mr.num_orders, 0), 2) AS avg_order_value,
    -- CAC (Customer Acquisition Cost)
    ROUND(mm.ad_spend / NULLIF(nc.new_customers, 0), 2) AS cac
FROM monthly_revenue mr
LEFT JOIN monthly_new_customers nc ON mr.month = nc.month
LEFT JOIN monthly_marketing mm ON mr.month = mm.month
ORDER BY mr.month;


-- 4. CONVERSION FUNNEL ANALYSIS


WITH customer_orders AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS num_orders
    FROM orders
    GROUP BY customer_id
)
SELECT 
    'Registered' AS stage,
    COUNT(*) AS customers,
    100.0 AS conversion_rate
FROM customers

UNION ALL

SELECT 
    'Activated (1st Order)' AS stage,
    COUNT(*) AS customers,
    ROUND(COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM customers) * 100, 2) AS conversion_rate
FROM customer_orders
WHERE num_orders >= 1

UNION ALL

SELECT 
    '2nd Order' AS stage,
    COUNT(*) AS customers,
    ROUND(COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM customers) * 100, 2) AS conversion_rate
FROM customer_orders
WHERE num_orders >= 2

UNION ALL

SELECT 
    '3rd Order' AS stage,
    COUNT(*) AS customers,
    ROUND(COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM customers) * 100, 2) AS conversion_rate
FROM customer_orders
WHERE num_orders >= 3

UNION ALL

SELECT 
    'Loyal (5+ Orders)' AS stage,
    COUNT(*) AS customers,
    ROUND(COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM customers) * 100, 2) AS conversion_rate
FROM customer_orders
WHERE num_orders >= 5;

-- 5. ACTIVATION RATE CALCULATION

SELECT 
    ROUND(
        COUNT(DISTINCT CASE WHEN o.customer_id IS NOT NULL THEN c.customer_id END)::NUMERIC /
        COUNT(DISTINCT c.customer_id) * 100, 
        2
    ) AS activation_rate,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT CASE WHEN o.customer_id IS NOT NULL THEN c.customer_id END) AS activated_customers
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- 6. CHURN RATE BY COHORT

WITH cohort_retention AS (
    -- Use the cohort retention query from #1
    -- Then calculate churn as 100 - retention_rate
    SELECT 
        cohort_month,
        months_since_registration,
        retention_rate,
        100 - retention_rate AS churn_rate
    FROM (
        -- Insert cohort retention query here
        SELECT * FROM cohort_retention_analysis
    ) cr
)
SELECT 
    cohort_month,
    months_since_registration,
    retention_rate,
    churn_rate,
    -- Flag retention cliffs (>15% drop from previous month)
    CASE 
        WHEN churn_rate - LAG(churn_rate) OVER (PARTITION BY cohort_month ORDER BY months_since_registration) > 15 
        THEN 'Cliff Detected'
        ELSE 'Normal'
    END AS retention_cliff_flag
FROM cohort_retention
ORDER BY cohort_month, months_since_registration;


-- 7. PRODUCT PERFORMANCE ANALYSIS

SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COUNT(DISTINCT o.order_id) AS num_orders,
    SUM(o.quantity) AS units_sold,
    SUM(o.revenue) AS revenue,
    SUM(o.cogs) AS cogs,
    SUM(o.gross_profit) AS gross_profit,
    ROUND((SUM(o.gross_profit) / NULLIF(SUM(o.revenue), 0)) * 100, 2) AS gross_margin,
    ROUND(SUM(o.revenue) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS avg_order_value
FROM products p
JOIN orders o ON p.product_id = o.product_id
GROUP BY 1, 2, 3
ORDER BY revenue DESC;

-- 8. CHANNEL PERFORMANCE (CAC, LTV, ROI)

WITH channel_revenue AS (
    SELECT 
        o.channel,
        COUNT(DISTINCT o.customer_id) AS active_customers,
        COUNT(DISTINCT o.order_id) AS num_orders,
        SUM(o.revenue) AS revenue,
        SUM(o.cogs) AS cogs,
        SUM(o.gross_profit) AS gross_profit
    FROM orders o
    GROUP BY o.channel
),
channel_customers AS (
    SELECT 
        channel,
        COUNT(DISTINCT customer_id) AS customers_acquired
    FROM customers
    GROUP BY channel
),
channel_marketing AS (
    SELECT 
        channel,
        SUM(ad_spend) AS ad_spend
    FROM marketing_costs
    GROUP BY channel
)
SELECT 
    cr.channel,
    cr.revenue,
    cr.cogs,
    cr.gross_profit,
    ROUND((cr.gross_profit / NULLIF(cr.revenue, 0)) * 100, 2) AS gross_margin,
    cr.active_customers,
    cr.num_orders,
    cc.customers_acquired,
    cm.ad_spend,
    -- CAC
    ROUND(cm.ad_spend / NULLIF(cc.customers_acquired, 0), 2) AS cac,
    -- LTV
    ROUND(cr.revenue / NULLIF(cc.customers_acquired, 0), 2) AS ltv,
    -- ROI
    ROUND(((cr.revenue - cm.ad_spend) / NULLIF(cm.ad_spend, 0)) * 100, 2) AS roi
FROM channel_revenue cr
JOIN channel_customers cc ON cr.channel = cc.channel
JOIN channel_marketing cm ON cr.channel = cm.channel;

-- 9. TIME TO FIRST VALUE (TTFV) ANALYSIS

WITH first_orders AS (
    SELECT 
        customer_id,
        MIN(order_date) AS first_order_date
    FROM orders
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    c.registration_date,
    fo.first_order_date,
    EXTRACT(DAY FROM AGE(fo.first_order_date, c.registration_date)) AS time_to_first_value_days,
    CASE 
        WHEN EXTRACT(DAY FROM AGE(fo.first_order_date, c.registration_date)) <= 7 THEN 'Fast (0-7 days)'
        WHEN EXTRACT(DAY FROM AGE(fo.first_order_date, c.registration_date)) <= 14 THEN 'Medium (8-14 days)'
        WHEN EXTRACT(DAY FROM AGE(fo.first_order_date, c.registration_date)) <= 30 THEN 'Slow (15-30 days)'
        ELSE 'Very Slow (30+ days)'
    END AS ttfv_segment
FROM customers c
LEFT JOIN first_orders fo ON c.customer_id = fo.customer_id
WHERE fo.first_order_date IS NOT NULL;

-- 10. ARPU AND ARPPU TREND ANALYSIS

WITH monthly_metrics AS (
    SELECT 
        DATE_TRUNC('month', o.order_date) AS month,
        COUNT(DISTINCT o.customer_id) AS active_customers,
        COUNT(DISTINCT c.customer_id) AS total_customers,
        SUM(o.revenue) AS revenue
    FROM orders o
    CROSS JOIN (SELECT COUNT(DISTINCT customer_id) AS customer_id FROM customers) c
    GROUP BY 1
)
SELECT 
    month,
    revenue,
    active_customers,
    -- ARPU (Average Revenue Per User - all registered users)
    ROUND(revenue / NULLIF(total_customers, 0), 2) AS arpu,
    -- ARPPU (Average Revenue Per Paying User - only active customers)
    ROUND(revenue / NULLIF(active_customers, 0), 2) AS arppu
FROM monthly_metrics
ORDER BY month;


