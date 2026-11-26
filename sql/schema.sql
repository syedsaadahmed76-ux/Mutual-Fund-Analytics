-- ============================================
-- MUTUAL FUND ANALYTICS DATABASE
-- Bluestock Data Analyst Internship
-- ============================================

PRAGMA foreign_keys = ON;


-- ============================================
-- 1. FUND DIMENSION TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    plan TEXT
);


-- ============================================
-- 2. INVESTOR DIMENSION TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS dim_investor (
    investor_id TEXT PRIMARY KEY,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL
);


-- ============================================
-- 3. DATE DIMENSION TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_value TEXT PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER
);


-- ============================================
-- 4. NAV FACT TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code INTEGER,
    nav_date TEXT,
    nav REAL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (nav_date)
        REFERENCES dim_date(date_value)
);


-- ============================================
-- 5. FUND PERFORMANCE FACT TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code INTEGER PRIMARY KEY,

    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,

    benchmark_3yr_pct REAL,

    alpha REAL,
    beta REAL,

    sharpe_ratio REAL,
    sortino_ratio REAL,

    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,

    aum_crore REAL,
    expense_ratio_pct REAL,

    morningstar_rating TEXT,
    risk_grade TEXT,

    expense_ratio_anomaly INTEGER,
    return_1yr_pct_anomaly INTEGER,
    return_3yr_pct_anomaly INTEGER,
    return_5yr_pct_anomaly INTEGER,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);


-- ============================================
-- 6. TRANSACTION FACT TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

    investor_id TEXT,
    transaction_date TEXT,
    amfi_code INTEGER,

    transaction_type TEXT,
    amount_inr REAL,

    payment_mode TEXT,
    kyc_status TEXT,

    FOREIGN KEY (investor_id)
        REFERENCES dim_investor(investor_id),

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (transaction_date)
        REFERENCES dim_date(date_value)
);


-- ============================================
-- INDEXES FOR BETTER QUERY PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_nav_amfi_code
ON fact_nav(amfi_code);

CREATE INDEX IF NOT EXISTS idx_nav_date
ON fact_nav(nav_date);

CREATE INDEX IF NOT EXISTS idx_transactions_date
ON fact_transactions(transaction_date);

CREATE INDEX IF NOT EXISTS idx_transactions_investor
ON fact_transactions(investor_id);

CREATE INDEX IF NOT EXISTS idx_transactions_fund
ON fact_transactions(amfi_code);


-- ============================================
-- SCHEMA CREATION COMPLETED
-- ============================================