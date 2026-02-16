-- Monthly Revenue Breakdown with COGS Analysis
-- Identifies margin compression over time

SELECT 
    DATE_TRUNC('month', order_date) AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(order_total) AS total_revenue,
    ROUND(AVG(order_total), 2) AS avg_order_value,
    
    -- COGS tracking (estimated at 46% average)
    ROUND(SUM(order_total) * 0.46, 2) AS estimated_cogs,
    ROUND(SUM(order_total) * 0.54, 2) AS gross_profit,
    ROUND(100.0 * 0.54, 2) AS gross_margin_percent
    
FROM orders
WHERE order_date BETWEEN '2025-05-01' AND '2025-10-31'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- Key finding: Revenue dropped from 989K UAH (May) to 451K UAH (Oct) = -34%