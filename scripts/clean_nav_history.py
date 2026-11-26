import pandas as pd
import glob
import os

# =====================================
# 1. FILE LOCATIONS
# =====================================

RAW_FOLDER = "data/raw"
PROCESSED_FOLDER = "data/processed"

os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Find NAV history CSV
files = glob.glob(
    os.path.join(RAW_FOLDER, "*nav_history*.csv")
)

if not files:
    raise FileNotFoundError("NAV history CSV not found!")

NAV_FILE = files[0]

print("Loading:", NAV_FILE)

# =====================================
# 2. LOAD DATA
# =====================================

df = pd.read_csv(NAV_FILE)

print("\nOriginal Records:", len(df))

print("\nOriginal Columns:")
print(df.columns.tolist())

# =====================================
# 3. CHECK REQUIRED COLUMNS
# =====================================

required_columns = ["amfi_code", "date", "nav"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# =====================================
# 4. CONVERT DATA TYPES
# =====================================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["nav"] = pd.to_numeric(
    df["nav"],
    errors="coerce"
)

df["amfi_code"] = pd.to_numeric(
    df["amfi_code"],
    errors="coerce"
)

# Remove invalid scheme codes and dates
df = df.dropna(
    subset=["amfi_code", "date"]
)

# =====================================
# 5. REMOVE DUPLICATES
# =====================================

before_duplicates = len(df)

df = df.drop_duplicates(
    subset=["amfi_code", "date"],
    keep="last"
)

duplicates_removed = before_duplicates - len(df)

# =====================================
# 6. VALIDATE NAV > 0
# =====================================

invalid_nav = (df["nav"] <= 0).sum()

# Convert invalid NAV values to missing
df.loc[df["nav"] <= 0, "nav"] = float("nan")

# =====================================
# 7. SORT DATA
# =====================================

df = df.sort_values(
    ["amfi_code", "date"]
)

# =====================================
# 8. FORWARD FILL MISSING NAV
# =====================================

missing_before = df["nav"].isna().sum()

df["nav"] = df.groupby(
    "amfi_code"
)["nav"].ffill()

missing_after = df["nav"].isna().sum()

# Remove records where NAV remains missing
df = df.dropna(subset=["nav"])

# =====================================
# 9. FINAL VALIDATION
# =====================================

assert (df["nav"] > 0).all()

assert not df.duplicated(
    subset=["amfi_code", "date"]
).any()

# =====================================
# 10. SAVE CLEANED DATA
# =====================================

output_file = os.path.join(
    PROCESSED_FOLDER,
    "clean_nav.csv"
)

df.to_csv(output_file, index=False)

# =====================================
# 11. CLEANING REPORT
# =====================================

print("\n" + "=" * 50)
print("NAV HISTORY CLEANING REPORT")
print("=" * 50)

print("Original Records:", len(pd.read_csv(NAV_FILE)))

print("Duplicates Removed:", duplicates_removed)

print("Invalid NAV Values:", invalid_nav)

print("Missing NAV Before Fill:", missing_before)

print("Missing NAV After Fill:", missing_after)

print("Final Records:", len(df))

print("Minimum NAV:", df["nav"].min())

print("Maximum NAV:", df["nav"].max())

print("\nSaved File:", output_file)

print("\nNAV CLEANING COMPLETED SUCCESSFULLY!")