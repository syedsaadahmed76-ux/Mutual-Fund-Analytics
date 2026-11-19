
import pandas as pd
import glob

# Load datasets
fund_file = glob.glob("data/raw/*fund_master*.csv")[0]
nav_file = glob.glob("data/raw/*nav_history*.csv")[0]

fund = pd.read_csv(fund_file)
nav = pd.read_csv(nav_file)

# Extract scheme codes
fund_codes = set(
    pd.to_numeric(fund["amfi_code"], errors="coerce")
    .dropna()
    .astype("int64")
)

nav_codes = set(
    pd.to_numeric(nav["amfi_code"], errors="coerce")
    .dropna()
    .astype("int64")
)

# Compare codes
matching = fund_codes.intersection(nav_codes)
missing = fund_codes.difference(nav_codes)

print("\n========== AMFI VALIDATION ==========")
print("Fund Master unique codes:", len(fund_codes))
print("NAV History unique codes:", len(nav_codes))
print("Matching codes:", len(matching))
print("Missing codes:", len(missing))

print("\nMissing AMFI Codes:")
print(sorted(missing))

print("\nValidation completed!")
