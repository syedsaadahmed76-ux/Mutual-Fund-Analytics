import pandas as pd
import os

# File path
file_path = "data/processed/clean_transactions.csv"

# Load cleaned dataset
df = pd.read_csv(file_path)

print("\n========== TRANSACTION DATA VALIDATION ==========")

# 1. Dataset information
print("\n1. DATASET INFORMATION")
print("Total Records:", len(df))
print("Total Columns:", len(df.columns))
print("Columns:", df.columns.tolist())

# 2. Missing values
print("\n2. MISSING VALUES")
print(df.isnull().sum())

# 3. Transaction type analysis
print("\n3. TRANSACTION TYPE DISTRIBUTION")
print(df["transaction_type"].value_counts())

# 4. Amount validation
print("\n4. AMOUNT VALIDATION")

df["amount_inr"] = pd.to_numeric(
    df["amount_inr"], errors="coerce"
)

print("Minimum Amount:", df["amount_inr"].min())
print("Maximum Amount:", df["amount_inr"].max())
print("Invalid Amounts:",
      ((df["amount_inr"].isna()) |
       (df["amount_inr"] <= 0)).sum())

# 5. Date validation
print("\n5. DATE VALIDATION")

date_col = (
    "transaction_date"
    if "transaction_date" in df.columns
    else "date"
)

if date_col not in df.columns:
    print("Date column not found!")
else:
    dates = pd.to_datetime(
        df[date_col], errors="coerce", dayfirst=True
    )

    print("Valid Dates:", dates.notna().sum())
    print("Invalid Dates:", dates.isna().sum())
    print("Earliest Date:", dates.min())
    print("Latest Date:", dates.max())

# 6. Duplicate validation
print("\n6. DUPLICATE VALIDATION")
print("Duplicate Records:", df.duplicated().sum())

# 7. KYC validation
print("\n7. KYC STATUS")

if "kyc_status" in df.columns:
    print(df["kyc_status"].value_counts(dropna=False))
else:
    print("KYC status column not found.")

# 8. Final report
print("\n========== FINAL VALIDATION REPORT ==========")

print("Dataset:", file_path)
print("Total Records:", len(df))
print("Validation Completed Successfully!")