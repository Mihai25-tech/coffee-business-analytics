-- Customer Lifetime Value (LTV) Calculation
-- Compares LTV to Customer Acquisition Cost (CAC)

WITH customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(order_total) AS total_revenue,
        MIN(order_date) AS first_purchase_date,
        MAX(order_date) AS last_purchase_date,
        DATEDIFF('day', MIN(order_date), MAX(order_date)) AS customer_lifespan_days
    FROM orders
    GROUP BY customer_id
)

SELECT 
    ROUND(AVG(total_revenue), 2) AS avg_ltv,
    ROUND(AVG(total_orders), 2) AS avg_orders_per_customer,
    ROUND(AVG(customer_lifespan_days), 0) AS avg_lifespan_days,
    
    -- Compare to CAC
    185 AS customer_acquisition_cost_uah,
    ROUND(AVG(total_revenue) - 185, 2) AS net_value_per_customer,
    
    -- LTV to CAC ratio
    ROUND(AVG(total_revenue) / 185, 2) AS ltv_to_cac_ratio
FROM customer_metrics;

-- Result: LTV = 98 UAH, CAC = 185 UAH → Negative unit economics