# Mutual Fund Analytics – Data Dictionary

## Project Overview
This data dictionary describes the tables and columns in the Bluestock Mutual Fund Analytics SQLite database.

**Database:** `bluestock_mf.db`

## 1. dim_fund

| Column | Data Type | Description |
|---|---|---|
| amfi_code | INTEGER | Unique AMFI scheme code |
| scheme_name | TEXT | Mutual fund scheme name |
| fund_house | TEXT | Asset management company |
| category | TEXT | Fund category |
| plan | TEXT | Scheme plan |

## 2. dim_investor

| Column | Data Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | City classification |
| age_group | TEXT | Investor age group |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Annual income in lakhs |

## 3. dim_date

| Column | Data Type | Description |
|---|---|---|
| date_value | TEXT | Date value |
| year | INTEGER | Calendar year |
| month | INTEGER | Month number |
| day | INTEGER | Day of month |

## 4. fact_nav

| Column | Data Type | Description |
|---|---|---|
| amfi_code | INTEGER | Mutual fund scheme code |
| nav_date | TEXT | NAV date |
| nav | REAL | Net Asset Value |

## 5. fact_performance

| Column | Data Type | Description |
|---|---|---|
| amfi_code | INTEGER | Mutual fund scheme code |
| return_1yr_pct | REAL | 1-year return percentage |
| return_3yr_pct | REAL | 3-year return percentage |
| return_5yr_pct | REAL | 5-year return percentage |
| benchmark_3yr_pct | REAL | 3-year benchmark return |
| alpha | REAL | Alpha performance measure |
| beta | REAL | Beta risk measure |
| sharpe_ratio | REAL | Sharpe ratio |
| sortino_ratio | REAL | Sortino ratio |
| std_dev_ann_pct | REAL | Annualized standard deviation |
| max_drawdown_pct | REAL | Maximum drawdown percentage |
| aum_crore | REAL | Assets under management in crore |
| expense_ratio_pct | REAL | Expense ratio percentage |
| morningstar_rating | TEXT | Morningstar rating |
| risk_grade | TEXT | Fund risk classification |
| expense_ratio_anomaly | INTEGER | Expense ratio anomaly flag |
| return_1yr_pct_anomaly | INTEGER | 1-year return anomaly flag |
| return_3yr_pct_anomaly | INTEGER | 3-year return anomaly flag |
| return_5yr_pct_anomaly | INTEGER | 5-year return anomaly flag |

## 6. fact_transactions

| Column | Data Type | Description |
|---|---|---|
| transaction_id | INTEGER | Unique transaction identifier |
| investor_id | TEXT | Investor identifier |
| transaction_date | TEXT | Transaction date |
| amfi_code | INTEGER | Mutual fund scheme code |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption |
| amount_inr | REAL | Transaction amount in INR |
| payment_mode | TEXT | Payment method |
| kyc_status | TEXT | Investor KYC status |

## Data Sources

- Fund master data
- Investor data
- NAV history
- Fund performance data
- Investor transaction data

## Database Relationships

- `dim_fund` connects to `fact_nav` through `amfi_code`.
- `dim_fund` connects to `fact_performance` through `amfi_code`.
- `dim_fund` connects to `fact_transactions` through `amfi_code`.
- `dim_investor` connects to `fact_transactions` through `investor_id`.
- `dim_date` connects to transaction and NAV dates.

## Tools Used

- Python
- SQLite
- SQL
- Pandas
- Power BI
