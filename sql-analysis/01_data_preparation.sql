-- Data Preparation and Cleaning
-- Coffee E-Commerce Analysis Project
-- Purpose: Clean and standardize transaction data from multiple sources

-- Remove duplicate orders
WITH duplicates_removed AS (
    SELECT DISTINCT
        order_id,
        order_date,
        customer_id,
        product_name,
        quantity,
        price,
        channel
    FROM raw_orders
)

-- Standardize channel names
, standardized_channels AS (
    SELECT *,
        CASE 
            WHEN channel ILIKE '%instagram%' THEN 'Instagram'
            WHEN channel ILIKE '%website%' THEN 'Website'
            WHEN channel ILIKE '%marketplace%' THEN 'Marketplace'
            ELSE 'Other'
        END AS channel_clean
    FROM duplicates_removed
)

-- Calculate order totals
SELECT 
    order_id,
    order_date,
    customer_id,
    product_name,
    quantity,
    price,
    quantity * price AS order_total,
    channel_clean AS channel
FROM standardized_channels
WHERE order_date IS NOT NULL
  AND customer_id IS NOT NULL
ORDER BY order_date;