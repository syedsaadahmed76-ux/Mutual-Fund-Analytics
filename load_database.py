
import sqlite3
import pandas as pd
import os

# ==========================================
# 1. FILE PATHS
# ==========================================

DB_PATH = "bluestock_mf.db"

DATA_FOLDER = "data/processed"

nav_file = os.path.join(DATA_FOLDER, "clean_nav.csv")
performance_file = os.path.join(DATA_FOLDER, "clean_performance.csv")
transactions_file = os.path.join(DATA_FOLDER, "clean_transactions.csv")

# ==========================================
# 2. LOAD CSV FILES
# ==========================================

nav = pd.read_csv(nav_file)
performance = pd.read_csv(performance_file)
transactions = pd.read_csv(transactions_file)

# Clean column names
for df in [nav, performance, transactions]:
    df.columns = df.columns.str.strip().str.lower()

print("CSV FILES LOADED SUCCESSFULLY")

print("NAV Records:", len(nav))
print("Performance Records:", len(performance))
print("Transaction Records:", len(transactions))

# ==========================================
# 3. CLEAN DATA TYPES
# ==========================================

# Convert AMFI codes
for df in [nav, performance, transactions]:
    df["amfi_code"] = pd.to_numeric(
        df["amfi_code"], errors="coerce"
    ).astype("Int64")

# Convert NAV dates
nav["date"] = pd.to_datetime(
    nav["date"], errors="coerce"
).dt.strftime("%Y-%m-%d")

# Convert transaction dates
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"], errors="coerce"
).dt.strftime("%Y-%m-%d")

# Convert amount
transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"], errors="coerce"
)

# Convert NAV
nav["nav"] = pd.to_numeric(nav["nav"], errors="coerce")

# ==========================================
# 4. PREPARE DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")

try:

    # Clear old records to prevent duplicates
    # when running this script again.

    conn.execute("DELETE FROM fact_transactions")
    conn.execute("DELETE FROM fact_nav")
    conn.execute("DELETE FROM fact_performance")
    conn.execute("DELETE FROM dim_investor")
    conn.execute("DELETE FROM dim_fund")
    conn.execute("DELETE FROM dim_date")

    # ======================================
    # 5. POPULATE FUND DIMENSION
    # ======================================

    fund_columns = [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "plan"
    ]

    funds = performance[fund_columns].copy()

    all_codes = pd.concat([
        performance["amfi_code"],
        nav["amfi_code"],
        transactions["amfi_code"]
    ]).dropna().unique()

    funds = funds.dropna(subset=["amfi_code"])
    funds = funds.drop_duplicates("amfi_code")

    missing_codes = set(all_codes) - set(funds["amfi_code"])

    if missing_codes:
        extra_funds = pd.DataFrame({
            "amfi_code": list(missing_codes),
            "scheme_name": None,
            "fund_house": None,
            "category": None,
            "plan": None
        })

        funds = pd.concat(
            [funds, extra_funds],
            ignore_index=True
        )

    funds.to_sql(
        "dim_fund", conn,
        if_exists="append", index=False
    )

    print("Fund dimension loaded:", len(funds))

    # ======================================
    # 6. POPULATE INVESTOR DIMENSION
    # ======================================

    investor_columns = [
        "investor_id",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "annual_income_lakh"
    ]

    investors = transactions[investor_columns].copy()

    investors = investors.dropna(subset=["investor_id"])
    investors["investor_id"] = (
        investors["investor_id"].astype(str).str.strip()
    )

    investors = investors.drop_duplicates("investor_id")

    investors.to_sql(
        "dim_investor", conn,
        if_exists="append", index=False
    )

    print("Investor dimension loaded:", len(investors))

    # ======================================
    # 7. POPULATE DATE DIMENSION
    # ======================================

    all_dates = pd.concat([
        nav["date"],
        transactions["transaction_date"]
    ]).dropna().unique()

    dates = pd.DataFrame({"date_value": all_dates})

    dates["year"] = pd.to_datetime(
        dates["date_value"]
    ).dt.year

    dates["month"] = pd.to_datetime(
        dates["date_value"]
    ).dt.month

    dates["day"] = pd.to_datetime(
        dates["date_value"]
    ).dt.day

    dates.to_sql(
        "dim_date", conn,
        if_exists="append", index=False
    )

    print("Date dimension loaded:", len(dates))

    # ======================================
    # 8. POPULATE NAV FACT TABLE
    # ======================================

    nav_data = nav[
        ["amfi_code", "date", "nav"]
    ].copy()

    nav_data = nav_data.dropna()

    nav_data = nav_data.rename(
        columns={"date": "nav_date"}
    )

    nav_data = nav_data.drop_duplicates(
        ["amfi_code", "nav_date"]
    )

    nav_data.to_sql(
        "fact_nav", conn,
        if_exists="append", index=False
    )

    print("NAV records loaded:", len(nav_data))

    # ======================================
    # 9. POPULATE PERFORMANCE FACT TABLE
    # ======================================

    performance_columns = [
        "amfi_code",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating",
        "risk_grade",
        "expense_ratio_anomaly",
        "return_1yr_pct_anomaly",
        "return_3yr_pct_anomaly",
        "return_5yr_pct_anomaly"
    ]

    performance_data = performance[
        performance_columns
    ].copy()

    performance_data = performance_data.dropna(
        subset=["amfi_code"]
    )

    performance_data = performance_data.drop_duplicates(
        "amfi_code"
    )

    performance_data.to_sql(
        "fact_performance", conn,
        if_exists="append", index=False
    )

    print(
        "Performance records loaded:",
        len(performance_data)
    )

    # ======================================
    # 10. POPULATE TRANSACTION FACT TABLE
    # ======================================

    transaction_columns = [
        "investor_id",
        "transaction_date",
        "amfi_code",
        "transaction_type",
        "amount_inr",
        "payment_mode",
        "kyc_status"
    ]

    transaction_data = transactions[
        transaction_columns
    ].copy()

    transaction_data = transaction_data.dropna(
        subset=[
            "investor_id",
            "transaction_date",
            "amfi_code",
            "amount_inr"
        ]
    )

    transaction_data["investor_id"] = (
        transaction_data["investor_id"].astype(str).str.strip()
    )

    transaction_data.to_sql(
        "fact_transactions", conn,
        if_exists="append", index=False
    )

    print(
        "Transaction records loaded:",
        len(transaction_data)
    )

    # ======================================
    # 11. VALIDATE DATABASE
    # ======================================

    print("\n========== DATABASE SUMMARY ==========")

    tables = [
        "dim_fund",
        "dim_investor",
        "dim_date",
        "fact_nav",
        "fact_performance",
        "fact_transactions"
    ]

    for table in tables:

        count = conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count} records")

    # Foreign key validation
    errors = conn.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    print("\nForeign Key Errors:", len(errors))

    if errors:
        print(errors[:10])
    else:
        print("All foreign keys validated successfully!")

    conn.commit()

    print("\nDATABASE INGESTION COMPLETED SUCCESSFULLY!")

except Exception as e:

    conn.rollback()

    print("\nDATABASE INGESTION FAILED!")
    print("Error:", e)

finally:

    conn.close()