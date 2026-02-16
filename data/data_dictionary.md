# Data Dictionary

Complete reference for all tables and columns in the Coffee E-Commerce Analytics dataset.

---

##  Tables Overview

| Table Name | Records | Description |
|------------|---------|-------------|
| `customers` | 1,685 | Customer registration and profile data |
| `orders` | 4,378+ | Transaction-level order data |
| `products` | ~50 | Product catalog |
| `marketing_costs` | 36 | Monthly marketing spend by channel (6 months × 6 channels) |

---

## 1. Customers Table

**Description:** Contains customer registration data and acquisition channel information.

| Column Name | Data Type | Nullable | Description | Example Values |
|-------------|-----------|----------|-------------|----------------|
| `customer_id` | VARCHAR(50) | NO | Unique customer identifier | CUST001, CUST002 |
| `registration_date` | DATE | NO | Date customer registered | 2025-05-15 |
| `channel` | VARCHAR(50) | NO | Customer acquisition channel | Instagram, Website, Marketplace |
| `customer_segment` | VARCHAR(50) | YES | Customer segment classification | Standard, Premium, VIP |

**Channel Values:**
- `Instagram` - Acquired via Instagram marketing
- `Website` - Acquired via direct website
- `Marketplace` - Acquired via third-party marketplace

**Data Quality Notes:**
- All customer_id values are unique
- No missing registration_date values
- Channel names standardized during cleaning

---

## 2. Orders Table

**Description:** Transaction-level data for all orders placed during May-October 2025.

| Column Name | Data Type | Nullable | Description | Example Values | Notes |
|-------------|-----------|----------|-------------|----------------|-------|
| `order_id` | VARCHAR(50) | NO | Unique order identifier | ORD00001 | Primary key |
| `customer_id` | VARCHAR(50) | NO | Customer who placed order | CUST001 | Foreign key to customers |
| `order_date` | DATE | NO | Date order was placed | 2025-05-20 | Range: 2025-05-01 to 2025-10-31 |
| `product_id` | VARCHAR(50) | YES | Product ordered | PROD001 | Foreign key to products |
| `product_name` | VARCHAR(200) | YES | Product name | Coffee Beans - Organic Fair Trade | Descriptive name |
| `category` | VARCHAR(100) | YES | Product category | Coffee Beans, Accessories, Tea | Grouped categories |
| `quantity` | INTEGER | NO | Number of units ordered | 1, 2, 5 | Must be > 0 |
| `price` | DECIMAL(10,2) | NO | Unit price in UAH | 450.00 | Price per unit |
| `revenue` | DECIMAL(10,2) | NO | Total order revenue | 900.00 | Calculated: price × quantity |
| `cogs` | DECIMAL(10,2) | NO | Cost of goods sold | 430.00 | Direct product cost |
| `gross_profit` | DECIMAL(10,2) | NO | Gross profit | 470.00 | Calculated: revenue - cogs |
| `channel` | VARCHAR(50) | YES | Sales channel | B2B (Wholesale), B2C (E-commerce + Social), Service | Revenue channel |

**Revenue Calculation:**
```
revenue = price × quantity
```

**Gross Profit Calculation:**
```
gross_profit = revenue - cogs
```

**Gross Margin Calculation:**
```
gross_margin_pct = (gross_profit / revenue) × 100
```

**Channel Categories:**
- `B2B (Wholesale)` - Wholesale orders (bulk purchases)
- `B2C (E-commerce + Social)` - Direct consumer sales (website + social media)
- `Service (Installation/Repair)` - Equipment installation and repair services

**Data Quality Notes:**
- All order_id values are unique
- Revenue values validated against (price × quantity)
- No negative or zero revenue values
- Orders outside May-October 2025 range excluded

---

## 3. Products Table

**Description:** Product catalog with category and pricing information.

| Column Name | Data Type | Nullable | Description | Example Values |
|-------------|-----------|----------|-------------|----------------|
| `product_id` | VARCHAR(50) | NO | Unique product identifier | PROD001 |
| `product_name` | VARCHAR(200) | NO | Product name | Organic Fair Trade Coffee Beans 1kg |
| `category` | VARCHAR(100) | NO | Product category | Coffee Beans, Accessories, Ground Coffee, Tea |
| `price` | DECIMAL(10,2) | YES | Standard retail price | 450.00 |

**Product Categories:**
- `Coffee Beans` - Whole bean coffee (various origins)
- `Ground Coffee` - Pre-ground coffee
- `Accessories` - Coffee equipment (grinders, frothers, scales)
- `Tea` - Tea products

**Data Quality Notes:**
- Category names standardized to Title Case
- Prices represent standard retail (actual order prices may vary)

---

## 4. Marketing Costs Table

**Description:** Monthly marketing spend and customer acquisition costs by channel.

| Column Name | Data Type | Nullable | Description | Example Values | Notes |
|-------------|-----------|----------|-------------|----------------|-------|
| `month` | DATE | NO | Month (first day of month) | 2025-05-01 | Format: YYYY-MM-01 |
| `channel` | VARCHAR(50) | NO | Marketing channel | Instagram, Website, Marketplace | Acquisition channel |
| `ad_spend` | DECIMAL(10,2) | NO | Advertising spend (UAH) | 45000.00 | Monthly ad budget |
| `cac` | DECIMAL(10,2) | NO | Customer Acquisition Cost | 239.78 | Cost per customer acquired |

**CAC Calculation:**
```
cac = ad_spend / new_customers_acquired
```

**Channel Values:**
- `Instagram` - Social media advertising
- `Website` - SEO, SEM, display ads
- `Marketplace` - Third-party marketplace fees
- `Referral` - Referral program costs
- `Email` - Email marketing costs
- `Other` - Other marketing channels

**Data Quality Notes:**
- Covers 6 months: May 2025 - October 2025
- All ad_spend values are positive
- CAC calculated based on actual new customer acquisitions

---

##  Key Metrics Definitions

### Customer Metrics

**Customer Lifetime Value (LTV)**
```
ltv = SUM(customer's total orders revenue)
```

**Customer Acquisition Cost (CAC)**
```
cac = total_ad_spend / new_customers_acquired
```

**LTV/CAC Ratio**
```
ltv_cac_ratio = ltv / cac
```
- **Healthy:** > 3.0
- **Warning:** 1.0 - 3.0
- **Critical:** < 1.0

**Activation Rate**
```
activation_rate = (customers_with_orders / total_customers) × 100
```

**Churn Rate**
```
churn_rate = (customers_inactive_in_period / total_customers_at_start) × 100
```

**Retention Rate**
```
retention_rate = (customers_active_in_period / cohort_size) × 100
```

### Revenue Metrics

**Gross Margin %**
```
gross_margin = (gross_profit / revenue) × 100
```

**ARPU (Average Revenue Per User)**
```
arpu = total_revenue / active_customers
```

**AOV (Average Order Value)**
```
aov = total_revenue / total_orders
```

### Time-Based Metrics

**Time to First Value (TTFV)**
```
ttfv_days = first_order_date - registration_date
```

**Customer Lifespan**
```
customer_lifespan_days = last_order_date - first_order_date
```

---

## Data Quality Standards

### Validation Rules

1. **Customers Table:**
   - No duplicate customer_id
   - All registration_date must be valid dates
   - Channel must be one of approved values

2. **Orders Table:**
   - No duplicate order_id
   - revenue = price × quantity (within 0.01 rounding)
   - gross_profit = revenue - cogs
   - All order_date within May-October 2025 range
   - All revenue > 0 and quantity > 0

3. **Products Table:**
   - No duplicate product_id
   - All categories standardized

4. **Marketing Costs Table:**
   - One row per month per channel
   - All ad_spend > 0
   - All CAC > 0

### Data Cleaning Process

See `python-analysis/data_cleaning.py` for full cleaning methodology.

**Key Steps:**
1. Remove duplicates
2. Standardize channel names
3. Validate calculations
4. Handle missing values
5. Remove invalid records

---

## Data Coverage

**Date Range:** May 1, 2025 - October 31, 2025 (6 months)

**Monthly Breakdown:**
- May 2025: 989K UAH revenue (peak)
- June 2025: ~850K UAH
- July 2025: ~780K UAH
- August 2025: ~650K UAH
- September 2025: ~550K UAH
- October 2025: 431K UAH (47% decline from peak)

---

## Important Notes

### Data Confidentiality

All data has been modified for confidentiality:
- Customer IDs anonymized
- Product names generalized
- Revenue figures scaled
- Exact dates may be shifted

**However:**
- Proportions and percentages are accurate
- Trend patterns are authentic
- Analysis methodology is real
- Business insights are genuine

### Wartime Context

Data collected during wartime operations with:
- 4-6 hours daily electricity
- Supplier disruptions
- Delivery challenges

These factors directly impact:
- COGS (increased due to supply chain issues)
- Customer retention (delivery reliability issues)
- Operational costs (higher than normal)

---

**Last Updated:** February 2026  
**Data Version:** 1.0 (Anonymized)
