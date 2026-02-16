-- Cohort Retention Analysis
-- Tracks customer retention by month of first purchase

WITH first_purchase AS (
    SELECT 
        customer_id,
        MIN(order_date) AS cohort_month
    FROM orders
    GROUP BY customer_id
),

customer_activity AS (
    SELECT 
        o.customer_id,
        fp.cohort_month,
        DATE_TRUNC('month', o.order_date) AS activity_month,
        DATE_PART('month', AGE(o.order_date, fp.cohort_month)) AS months_since_first
    FROM orders o
    JOIN first_purchase fp ON o.customer_id = fp.customer_id
),

cohort_size AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_customers
    FROM first_purchase
    GROUP BY cohort_month
)

SELECT 
    ca.cohort_month,
    cs.cohort_customers,
    ca.months_since_first AS month_number,
    COUNT(DISTINCT ca.customer_id) AS retained_customers,
    ROUND(100.0 * COUNT(DISTINCT ca.customer_id) / cs.cohort_customers, 2) AS retention_rate
FROM customer_activity ca
JOIN cohort_size cs ON ca.cohort_month = cs.cohort_month
GROUP BY ca.cohort_month, cs.cohort_customers, ca.months_since_first
ORDER BY ca.cohort_month, ca.months_since_first;