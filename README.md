# Coffee E-Commerce Business Analytics Dashboard
 
This analysis covers May-October 2025 operations during active conflict. The sharp revenue decline in September-October reflects escalated infrastructure attacks limiting electricity availability to 4 hours daily, ultimately leading to business closure. The project demonstrates financial modeling and analytical capabilities in crisis conditions.

**Live Dashboard:** [View on Tableau Public](https://public.tableau.com/app/profile/mykhailo.busniak/)
## Project Overview

This project is based on my 6 months working as a data analyst for a small coffee e-commerce business in Ukraine. All data has been modified to protect confidentiality, but the business patterns, challenges, and analysis approach are real.

The company operated three revenue channels: direct-to-consumer (website and social media), wholesale (B2B), and instalation/repair services. I built this dashboard to show end-to-end analytics work, from cleaning messy transaction data and building financial models in Excel, to creating interactive Tableau dashboards that helped the business understand what was happening.

**Key Numbers:**
- 4.67M UAH total revenue across 6 months
- 1,685 unique customers
- 3,470 transactions
- 3 revenue channels: B2C (50%), B2B (37%), Service (13%)
- 166K UAH net loss

The goal was to identify what's driving the losses and where the retention problems are.
## What I Found
### Revenue Decline
Revenue declined 47% from July peak (989K→431K) due to intensified missile strikes and critical infrastructure damage limiting electricity to 4h/day. Despite wartime disruption, maintained 43.8% gross margin through operational resilience. All three channels showed the same pattern — this wasn't a channel-specific issue, it was market-wide.
### Customer Retention Problem
Only 65% of customers make it past their first month. By month 5, we're down to 9.8%. The business is losing 90% of customers within half a year.

Breaking this down:
- Month 0: 65% active (35% churn immediately)
- Month 1: 44% active (56% total churn)
- Month 2: 33% active (67% total churn)
- Month 3: 25% active (75% total churn)
- Month 5: 9.8% active (90% total churn)

These numbers match e-commerce benchmarks for Ukraine during 2025, accounting for war impact.

### Profitability Issues
Despite generating 4.67M in revenue, the business lost 645K UAH. The main cost drivers:
- COGS: 2.217M (47% of revenue)
- Payroll: 1.23M (10-person team)
- Marketing: 496K
- Operating expenses: 609K

The team built a reserve fund (6% of monthly revenue set aside), which reached 280K by October. This covers about one month of fixed costs.

### Marketing Efficiency
Customer acquisition cost averaged 240 UAH per customer. Marketing spend ranged from 8-10% of revenue in good months, dropping to 7% as things tightened in fall.

The business brought in 1,685 new customers over 6 months:
- May: 400 new buyers (CAC: 197 UAH)
- October: 125 new buyers (CAC: 240 UAH)

Channel breakdown: 80% B2C, 20% B2B.
## Dashboard Breakdown

### Dashboard 1: Executive Overview
Shows the big picture. Six KPI cards at the top (margin, customers, AOV, revenue, CAC, churn), monthly revenue trends by channel, cohort retention heatmap, and a geographic sales map for Ukraine.

The retention heatmap is the key visual here. You can immediately see the drop from 65% to 9.8% across cohorts.

### Dashboard 2: Customer Analytics
Deep dive into customer behavior. Full cohort retention analysis, conversion funnel showing how customers move from first purchase to loyal status, and churn rate trends over time.

Only 6% of customers make 4+ orders, which is the definition of "loyal" for this business.

### Dashboard 3: Financial Performance
P&L waterfall chart showing the flow from 4.67M revenue down to -166K net loss. Also includes revenue breakdown by channel and the largest expense categories.

The waterfall makes it clear: COGS and payroll are eating most of the revenue.

### Dashboard 4: Product Performance
Product categories ranked by revenue (Coffee Beans leads with 710K), plus an interactive treemap of the top N most profitable products. You can adjust the parameter to show anywhere from 5 to 20 products.
Coffee Grinder was the single highest-revenue product at 232K.
## Technical Approach
### Data Preparation
Started with transaction data across three channels. Cleaned duplicates, standardized date formats (there were 5 different formats in the source data), and built the financial model in Excel before moving to Tableau.

Excel workbook includes:
- P&L statement with monthly breakdown
- Stress test scenarios for war escalation
- Revenue stream analysis with team capacity mapping
- Staff structure and costs (including 22% ESV Ukrainian social tax)
- Marketing spend and CAC calculations
- Churn and retention analysis by cohort
- Product performance by category
### Tableau Implementation
Built calculated fields for:
- Cohort analysis (using FIXED LOD expressions)
- Retention rates by time period
- Month-over-month growth percentages
- Customer segmentation (New/Returning/Loyal)
- Profit margins by product
Dashboard actions:
- Navigation bar to move between the four dashboards
- Filter actions (click a channel in one chart to filter others)
- Highlight actions (hover over a data point to highlight related data)
- Parameter controls for the Top N product filter
The goal was to make it easy to explore the data without overwhelming someone who just wants the executive summary.
## Business Recommendations

Based on this analysis, here's what I'd focus on:
**Fix Retention First**
With 65% churn after the first purchase, acquisition costs are wasted. The business needs:
- Email campaigns targeting first-time buyers in their second week
- Loyalty program for customers who make 2+ orders
- Analysis of what the 6% who stay are buying differently
**Address Seasonal Decline**
Revenue fell 47% from summer to fall. This could be:
- Seasonal demand (people drink less iced coffee?)
- Marketing budget cuts reducing new customer flow
- Macro factors (war escalation in August per the stress test sheet)
I'd dig into what drove the July peak to see if it's replicable.
**Cost Structure**
At 57% COGS, margins are thin. Options:
- Negotiate better supplier terms
- Focus on higher-margin products (Accessories at 42% vs Coffee Beans at 44%)
- Reduce the Service channel (lowest margin, highest operational complexity)
The Excel model shows that cutting the Service channel would save 47K/month in payroll.
## Data Sources and Methodology
**Data Period:** May 1 - October 31, 2025  
**Transaction Count:** 3,470 orders  
**Customer Count:** 1,685 unique buyers  
**Channels:** B2C (E-commerce + Social), B2B (Wholesale), Service (Gifts/Subscriptions)
### Metrics Defined
**Retention Rate:**
Retention(Month M) = Customers Active in Month M / Total Cohort Size

**Churn Rate:**
Churn(Month M) = 1 - Retention(Month M)

**Customer Acquisition Cost:**
CAC = Total Marketing Spend / New Customers Acquired

**Gross Profit Margin:**
GP Margin = (Revenue - COGS) / Revenue

### Cohort Methodology
Customers are grouped by the month of their first purchase. Each cohort is tracked for up to 6 months to measure retention over time. For example, the May cohort can be tracked through October, while the October cohort only has month 0 data.
## Project Timeline

**Week 1:** Gathered transaction data, customer records, and product catalog  
**Week 2:** Cleaned data (removed 847 duplicates, fixed date formats, validated totals), built Excel financial model with P&L, stress scenarios, and cohort analysis
**Week 3:** Created Tableau dashboards and calculated fields, added interactivity, refined visualizations, published to Tableau Public

Total time: about 72 hours over 3 weeks.
## Skills Demonstrated
**Data Analysis:**
- Financial modeling (P&L structure, margin analysis)
- Cohort analysis and retention tracking
- Customer segmentation
- Product profitability analysis
**Tableau:**
- LOD expressions (FIXED for cohort calculations)
- Table calculations (running totals, percent of total)
- Parameters (Top N filter)
- Dashboard actions (navigation, filtering, highlighting)
- Geographic mapping
**Business Intelligence:**
- KPI selection and tracking
- Executive reporting
- Insight generation from raw data
- Actionable recommendations
## Files in This Repository
/images
  - dashboard-1-executive.png
  - dashboard-2-customer.png
  - dashboard-3-financial.png
  - dashboard-4-products.png

/data
  - Coffee_Business_Analytics.xlsx (source calculations)
README.md (this file)

## Links

**Live Dashboard:** https://public.tableau.com/app/profile/mykhailo.busniak/

**My LinkedIn:** https://www.linkedin.com/in/mykhailo-busniak-data-analyst/  
## Notes
This project is based on real work I did as a junior data analyst for a Ukrainian coffee e-commerce company from May to October 2025. I was responsible for tracking performance, building financial reports, and analyzing customer behavior.
All specific numbers have been modified for confidentiality, but the business scenario is accurate: a small 10-person team trying to grow during wartime conditions, dealing with retention problems and thin margins. The analysis challenges I faced were real - messy data, multiple revenue streams, and pressure to show what's actually driving the losses.
The Excel model includes assumptions about war impact because that was part of the job. August showed revenue drops when there was frontline escalation.

I'm publishing this as a portfolio piece to show I can work with realistic business data and deliver analysis that's actually useful, not just pretty charts.

## What I Learned
**Data cleaning takes longer than you think.** When I started this job, I thought I'd be doing analysis from day one. Instead, I spent the first 2 weeks cleaning transaction exports - fixing text in revenue columns, reconciling 5 different date formats from different sales channels, hunting down duplicate orders. No one warns you about this in tutorials.

**Context matters more than perfect numbers.** The retention rates looked terrible on paper - losing 90% of customers in 6 months. But when I researched Ukrainian e-commerce benchmarks during the war, I found this was actually normal. Retention dropped 15-20% across the industry in 2024-2025. Knowing that completely changed what I recommended to the owner.

**Simple dashboards win.** My first version tried to show everything I'd calculated. Revenue by channel by product by region by week. The owner took one look and asked "what should I do about this?" I learned to cut ruthlessly. If a chart doesn't support a specific decision, it's just noise. The final version shows what matters: we're losing customers too fast, and costs are too high relative to revenue.

**Excel before Tableau.** I wanted to jump straight into Tableau, but the business needed financial models first. P&L structure, stress scenarios, team capacity planning. All of that happened in Excel with formulas the owner could modify. Tableau came later for visualization and exploration.

**Last Updated:** 10 February 2026  
**Created By:** Mike Busniak  
**Location:** London, UK
