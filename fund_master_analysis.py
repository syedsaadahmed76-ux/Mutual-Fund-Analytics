
import pandas as pd
import glob
import os

# Find fund master CSV
files = glob.glob("data/raw/*fund_master*.csv")

if not files:
    raise FileNotFoundError("Fund master CSV not found")

fund = pd.read_csv(files[0])

print("\nFUND MASTER SHAPE")
print(fund.shape)

print("\nCOLUMN NAMES")
print(fund.columns.tolist())

print("\nDATA TYPES")
print(fund.dtypes)

# Explore categorical columns
for col in fund.select_dtypes(include="object").columns:
    print(f"\nUnique values in {col}:")
    print(fund[col].nunique())
    print(fund[col].dropna().unique()[:20])

print("\nMISSING VALUES")
print(fund.isnull().sum())

print("\nDUPLICATE ROWS")
print(fund.duplicated().sum())


print("\n========== SCHEME CODE ANALYSIS ==========")

print("\nFund Master Columns:")
print(fund.columns.tolist())

# Identify scheme/code-related columns
for col in fund.columns:
    if "scheme" in col.lower() or "code" in col.lower():
        print(f"\nColumn: {col}")
        print(fund[col].head(10).tolist())

print("\n========== FUND HOUSE ANALYSIS ==========")

for col in fund.columns:
    if "house" in col.lower():
        print(fund[col].nunique())
        print(fund[col].dropna().unique())

print("\n========== CATEGORY ANALYSIS ==========")

for col in fund.columns:
    if "categor" in col.lower() or "risk" in col.lower():
        print(f"\n{col}")
        print(fund[col].value_counts(dropna=False))


print("\n========== ALL FUND MASTER COLUMNS ==========")

for col in fund.columns:
    print(col)

print("\n========== POSSIBLE SCHEME CODE COLUMNS ==========")

for col in fund.columns:
    if "scheme" in col.lower():
        print("\nColumn:", col)
        print(fund[col].head(15).to_string(index=False))

print("\n========== NAV HISTORY FILE ==========")

import glob
import os

nav_files = glob.glob("data/raw/*nav_history*.csv")

for file in nav_files:
    nav = pd.read_csv(file)
    print("\nFile:", os.path.basename(file))
    print("Shape:", nav.shape)
    print("Columns:", nav.columns.tolist())
    print(nav.head())


print("\n========== FUND MASTER SCHEME CODE ==========")

for col in fund.columns:
    if "code" in col.lower() or "scheme" in col.lower():
        print("\nColumn:", col)
        print("Data type:", fund[col].dtype)
        print(fund[col].head(15).to_string(index=False))
