-- Channel Performance Analysis
-- Compares revenue and customer behavior by marketing channel

WITH channel_metrics AS (
    SELECT 
        channel,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS unique_customers,
        SUM(order_total) AS total_revenue,
        ROUND(AVG(order_total), 2) AS avg_order_value
    FROM orders
    GROUP BY channel
),

channel_retention AS (
    SELECT 
        o1.channel,
        COUNT(DISTINCT o1.customer_id) AS first_time_buyers,
        COUNT(DISTINCT o2.customer_id) AS repeat_buyers
    FROM orders o1
    LEFT JOIN orders o2 
        ON o1.customer_id = o2.customer_id 
        AND o2.order_date > o1.order_date
    WHERE o1.order_date = (
        SELECT MIN(order_date) 
        FROM orders 
        WHERE customer_id = o1.customer_id
    )
    GROUP BY o1.channel
)

SELECT 
    cm.channel,
    cm.total_orders,
    cm.unique_customers,
    cm.total_revenue,
    cm.avg_order_value,
    cr.repeat_buyers,
    ROUND(100.0 * cr.repeat_buyers / cr.first_time_buyers, 2) AS repeat_purchase_rate
FROM channel_metrics cm
JOIN channel_retention cr ON cm.channel = cr.channel
ORDER BY cm.total_revenue DESC;