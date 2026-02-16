# Excel Financial Model

## What's In Here

I built this model to track the coffee shop's finances during wartime when everything was chaotic. Owner needed to know how long cash would last and whether the business was viable.

## The Sheets

### P&L Statement
Monthly breakdown of revenue and expenses.

**Revenue tracking:**
- Sales by channel (B2C, B2B, Service)
- Product categories
- Monthly trends

**Costs:**
- COGS (cost of goods sold) - this jumped to 47.8% which was a major problem
- Marketing spend
- Payroll
- Delivery costs (expensive during wartime)
- Rent and utilities
- Other operating expenses

**Bottom line:**
- Gross profit
- Operating profit
- Net profit (we were losing money most months)

### Cash Flow Analysis
Tracked cash in vs cash out.

During wartime with limited electricity and unreliable operations, this was critical. Owner needed to know if we'd run out of cash.

**Tracked:**
- Cash from sales
- Cash spent on inventory
- Marketing spend
- Fixed expenses
- Cash runway (months until money runs out)

At the rate we were burning cash, runway was about 8-9 months.

### Gross Margin Trends
Month by month margin tracking.

**Problem I found:**
- Started at 54% (healthy)
- Dropped to 39% by October (bad)
- Cause: COGS increased due to supplier issues during electricity crisis

**Suppliers were charging more because:**
- Fuel costs up (delivery difficult)
- Storage costs up (no refrigeration without power)
- Smaller order quantities (couldn't guarantee stable operations)

### Scenario Planning
Built 3 scenarios to help owner make decisions.

**Best Case:**
- Fix retention (2nd purchase rate from 38% to 55%)
- Reduce COGS back to 42%
- Cut marketing spend by 40%
- Result: Break even in 3 months, profitable after

**Base Case:**
- Improve retention slightly (38% to 45%)
- COGS stays at 47%
- Keep current marketing spend
- Result: Still losing money, 6 months runway

**Worst Case:**
- Retention stays at 38%
- COGS increases to 50%
- Revenue continues declining
- Result: Out of cash in 4 months

Owner used this to decide to pause ads and focus on existing customers.

### Key Assumptions
Numbers I used for calculations.

**Revenue:**
- Average order value: 381 UAH
- Monthly customers (declining): 450 → 180
- Repeat purchase rate: 38%

**Costs:**
- COGS: 47.8% (should be 40-45%)
- CAC: 239.78 UAH per customer
- Fixed costs: ~150K UAH per month (rent, payroll, utilities)

**Wartime factors:**
- Operational hours: 4-6 per day (limited by electricity)
- Delivery success rate: 85% (vs 98% in normal times)
- Supplier reliability: 70% (frequent stockouts)

## How to Use It

1. Open `Coffee_Business_Analytics.xlsx` in `/data` folder
2. Go to financial model sheets
3. Update assumptions in yellow cells if needed
4. Scenarios automatically recalculate

**Key cells to watch:**
- Monthly revenue (declining trend)
- COGS percentage (goal: get below 45%)
- Cash balance (how many months left)
- Monthly burn rate

## What I Learned Building This

Financial models during crisis need to be simple. Owner didn't have time for complex forecasts.

The most valuable output was the cash runway calculation. Once owner saw "4 months at current burn rate", decision to cut marketing spend became obvious.

Also learned that sometimes the most important number is the one that tells you to stop doing something, not what to do more of.

## Files

Main Excel file: `/data/Coffee_Business_Analytics.xlsx`

Sheets:
- P&L Statement
- Cash Flow
- Gross Margin Analysis
- Scenario Planning
- Assumptions

---

Built this in Excel because:
1. Owner already used Excel
2. Easy to update
3. Can share without special software
4. Financial people understand Excel better than Python

Not everything needs to be in Python or SQL.
