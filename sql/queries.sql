
-- 1. Top 5 mutual funds by AUM
SELECT scheme_name, fund_house, aum_crore
FROM dim_fund
JOIN fact_performance USING (amfi_code)
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT
    strftime('%Y-%m', nav_date) AS month,
    AVG(nav) AS average_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- 3. SIP investment growth by year
SELECT
    strftime('%Y', transaction_date) AS year,
    SUM(amount_inr) AS sip_investment
FROM fact_transactions
WHERE UPPER(transaction_type) = 'SIP'
GROUP BY year
ORDER BY year;

-- 4. Transactions by state
SELECT
    i.state,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount_inr) AS total_investment
FROM fact_transactions t
JOIN dim_investor i
    ON t.investor_id = i.investor_id
GROUP BY i.state
ORDER BY total_investment DESC;

-- 5. Funds with expense ratio below 1%
SELECT
    scheme_name,
    expense_ratio_pct,
    aum_crore
FROM dim_fund
JOIN fact_performance USING (amfi_code)
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;
