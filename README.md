# Coffee E-Commerce Analytics Project

Analysis of 6 months of e-commerce data for Ukrainian coffee startup (May - October 2025)

[View Live Dashboards](https://public.tableau.com/app/profile/mykhailo.busniak/viz) | [SQL Queries](./sql-analysis/) | [Python Code](./python-analysis/)

---

## What This Project Is About

I worked as a data analyst for a Ukrainian coffee startup during wartime. They were losing revenue fast and the owner thought they needed more marketing.

Turns out the real problem was completely different.

**The Situation:**
- 6 months of data (May - Oct 2025)
- 1,685 customers
- 4.67M UAH in revenue
- Operating with 4-6 hours of electricity per day (wartime constraints)

**What I Found:**
- Revenue dropped 47% (989K → 431K UAH)
- 69% of customers never made a second purchase
- Cost to acquire customer (239 UAH) was higher than what they spent (average LTV: 98 UAH)
- Margins were getting squeezed (COGS jumped to 47.8%)

The owner wanted to spend MORE on ads. The data said that would make things worse.

---

## Key Numbers

### Revenue & Customers
- Peak revenue: 989K UAH (July)
- Final revenue: 431K UAH (October)
- Revenue decline: -47% over 3 months
- Total customers: 1,685
- Active by end: 180 (down from 450)

### The Retention Problem
- After 1st purchase: 42% came back
- After 5 months: only 9% still active
- 2nd purchase rate: 38% (62% churn)
- Loyal customers (4+ orders): 6%

### Unit Economics
- Customer Acquisition Cost: 239.78 UAH
- Average Customer Lifetime Value: 98 UAH
- LTV/CAC ratio: 0.41 (should be > 3.0)
- Average Order Value: 381 UAH
- Gross Margin: 43.75% (declining)

---

## What I Built

### 1. Tableau Dashboards (4 dashboards)

**Executive Overview**
- Main KPIs: revenue, customers, margins, CAC
- Revenue trend showing the 47% drop
- Regional breakdown (Ukraine map)
- Cohort retention heatmap

**Customer Retention**
- Cohort analysis by month
- Conversion funnel visualization
- Churn tracking

**Financial Performance**
- P&L breakdown (waterfall chart)
- Revenue by channel
- Expense categories
- Monthly margin trends

**Product Analysis**
- Revenue by category
- Top products by profit
- Margin analysis

[View on Tableau Public →](https://public.tableau.com/app/profile/mykhailo.busniak/viz)

### 2. SQL Analysis (5 queries)

**Cohort Retention Analysis** - Tracking how many customers come back each month

**LTV & Unit Economics** - Customer profitability analysis (found that most customers were unprofitable)

**Monthly KPIs** - Revenue, margins, CAC tracking month by month

**Conversion Funnel** - Where customers drop off (62% after 1st purchase)

**Channel Performance** - Which marketing channels actually made money

All queries use CTEs, window functions, and cohort analysis techniques.

### 3. Python Data Cleaning

Cleaned messy data from multiple sources:
- Fixed duplicate customer IDs
- Standardized channel names (Instagram/Website/Marketplace)
- Validated revenue calculations
- Removed invalid orders
- Handled missing dates

### 4. Excel Financial Model

Built P&L tracking model with:
- Monthly revenue and expense breakdown
- Cash flow projections
- Gross margin analysis
- Scenario planning (best/base/worst case)
- Runway calculations

---

## Project Structure

```
coffee-business-analytics/
├── README.md
├── data/
│   ├── Coffee_Business_Analytics.xlsx
│   └── data_dictionary.md
├── sql-analysis/
│   ├── 01_cohort_retention_analysis.sql
│   ├── 02_customer_ltv_unit_economics.sql
│   ├── 03_monthly_kpis.sql
│   ├── 04_conversion_funnel_analysis.sql
│   └── 05_channel_performance.sql
├── python-analysis/
│   └── data_cleaning.py
├── excel-models/
│   └── Financial_Model_README.md
├── tableau-dashboards/
│   └── README.md
└── images/
    └── (dashboard screenshots)
```

---

## What I Recommended

**Stop spending on ads** - CAC was already too high. Acquiring more customers who churn after first purchase just burns more money.

**Fix the delivery experience** - During wartime with limited electricity, delivery was unreliable. This killed retention.

**Re-engage existing customers** - Cheaper than acquiring new ones. We had 1,685 people who bought once. Getting them to buy again costs 0 UAH in CAC.

**Renegotiate with suppliers** - COGS jumped from 40-45% (normal) to 47.8% due to wartime supply chain issues. Fixing this would save ~275K UAH.

**Focus on retention before acquisition** - If we could improve 2nd purchase rate from 38% to 50%, unit economics would actually work.

---

## How to Use This Repo

### SQL Queries

Requirements: PostgreSQL 12+, MySQL 8.0+, or SQL Server 2019+

Run queries in order:
```sql
\i sql-analysis/01_cohort_retention_analysis.sql
\i sql-analysis/02_customer_ltv_unit_economics.sql
\i sql-analysis/03_monthly_kpis.sql
\i sql-analysis/04_conversion_funnel_analysis.sql
\i sql-analysis/05_channel_performance.sql
```

### Python Cleaning Script

```bash
pip install pandas numpy openpyxl
python python-analysis/data_cleaning.py
```

### Tableau Dashboards

View live on [Tableau Public](https://public.tableau.com/app/profile/mykhailo.busniak/viz) or download the .twbx file to open in Tableau Desktop.

---

## Important Notes

**Data Confidentiality**

All data has been modified:
- Customer IDs anonymized
- Revenue figures scaled
- Product names generalized

The analysis methodology and insights are real. This represents actual work from a 6-month analyst role.

**Wartime Context**

This analysis happened during difficult conditions:
- 4-6 hours of daily electricity
- Supplier disruptions (caused COGS increase)
- Delivery challenges (hurt retention)

These factors directly affected the metrics.

---

## Skills Used

**Technical:**
- SQL: Complex queries, CTEs, window functions, cohort analysis
- Python: Data cleaning with pandas, data validation
- Tableau: Interactive dashboards, LOD calculations, parameters
- Excel: Financial modeling, Power Query, scenario analysis

**Business:**
- Root cause analysis (identified retention problem vs marketing problem)
- Unit economics (CAC vs LTV analysis)
- Strategic recommendations based on data

**Approach:**
1. Understood the business problem (owner thought marketing was the issue)
2. Analyzed the data (found retention was the real problem)
3. Quantified the impact (47% revenue drop, 69% churn)
4. Made actionable recommendations (fix retention before spending on ads)

---

## Contact

**Mike Busniak**

LinkedIn: [linkedin.com/in/mykhailo-busniak-data-analyst](https://www.linkedin.com/in/your-profile)

Email: busnyak41@gmail.com

GitHub: [github.com/Mihai25-tech](https://github.com/Mihai25-tech)

Tableau: [public.tableau.com/app/profile/mykhailo.busniak](https://public.tableau.com/app/profile/mykhailo.busniak/viz)

---

## License

MIT License - see LICENSE file

---

**Built during 6 months working for Ukrainian coffee startup under wartime conditions**

Last updated: February 2026
