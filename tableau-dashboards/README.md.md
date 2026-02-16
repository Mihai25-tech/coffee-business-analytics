# Tableau Dashboards

## View Live

All 4 dashboards are published on Tableau Public:

**[View All Dashboards →](https://public.tableau.com/app/profile/mykhailo.busniak/viz)**

---

## The Dashboards

### 1. Executive Overview

Main dashboard with high-level metrics.

**What's in it:**
- Top KPI cards: Gross Margin (43.75%), Total Customers (1,685), Revenue (4.67M UAH), Average Order Value (381 UAH), CAC (239.78 UAH)
- Revenue trend line chart showing the drop from 989K to 431K (47% decline)
- Ukraine map with regional sales distribution
- Cohort retention heatmap (shows the 69% churn problem)

**Why I built it:**
Owner needed one place to see if the business was healthy. This showed at a glance that it wasn't - revenue dropping, margins compressing, retention terrible.

---

### 2. Customer Retention Analysis

Deep dive into why customers weren't coming back.

**What's in it:**
- Cohort retention heatmap (Month 0 through Month 5)
- Conversion funnel showing drop-off at each stage
- Churn rate trends
- Time between purchases analysis

**Key finding here:**
Only 9% of customers were still active after 5 months. The biggest drop was between first and second purchase - 62% never came back.

This killed any hope of positive unit economics with CAC at 239 UAH.

---

### 3. Financial Performance (P&L)

Where the money was going.

**What's in it:**
- P&L waterfall chart (Revenue → COGS → Expenses → Net Profit)
- Revenue breakdown by channel (B2C: 50.2%, B2B: 37.3%, Service: 12.5%)
- Expense categories bar chart
- Monthly gross margin trend (declining from 54% to 39%)

**What this showed:**
We were losing money. Net loss of 165K UAH over 6 months. COGS at 47.8% was eating margins.

Biggest expense was delivery costs during wartime - unreliable and expensive.

---

### 4. Product Performance

Which products were actually making money.

**What's in it:**
- Product category revenue breakdown (Coffee Beans: 34% of revenue)
- Top 10 most profitable products (treemap)
- Margin analysis by product
- Sales volume vs profit scatter plot

**Insight:**
Organic Fair Trade coffee was the winner - highest margin product at 23.7K profit. But we were spending too much marketing low-margin accessories that people bought once and never came back for.

---

## Technical Stuff

Built using:
- **LOD calculations** for cohort retention (Month 0 cohort size vs Month 5 active)
- **Parameters** for dynamic date filtering
- **Calculated fields** for retention rates, LTV/CAC ratios
- **Custom color palette** to match coffee theme

Data source is Excel file with 4 tables:
- customers
- orders  
- products
- marketing_costs

Connected them using relationships on customer_id and product_id.

---

## Download to Explore

Want to dig into the data yourself?

1. Go to [Tableau Public link](https://public.tableau.com/app/profile/mykhailo.busniak/viz)
2. Click "Download" button (top right of any dashboard)
3. Opens in Tableau Desktop or Tableau Reader (free)

You can then filter by different date ranges, channels, products, etc.

---

## Why Tableau?

Owner wasn't technical. Couldn't send them SQL queries or Python notebooks.

Needed something interactive they could explore themselves. Tableau let them:
- Click on any month to see details
- Filter by channel or product
- Export charts for presentations
- Share with investors

Also Tableau Public is free and looks professional, which matters when you're trying to show your work to potential employers.

---

## Screenshots

Screenshots of all 4 dashboards are in `/images/` folder:
- `dashboard_executive.png`
- `dashboard_retention.png`
- `dashboard_financial.png`
- `dashboard_product.png`

---

Built these dashboards over 2 weeks while working remotely during daily electricity blackouts. Some days only had 4 hours of power, so had to work in chunks.

Learned a lot about building dashboards under pressure when stakeholder needs answer NOW but power might cut out in 30 minutes.
