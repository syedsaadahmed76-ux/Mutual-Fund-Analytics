
import pandas as pd
import os
import glob

# File paths
raw_folder = "data/raw"
output_folder = "data/processed"

os.makedirs(output_folder, exist_ok=True)

# Find source CSV
files = glob.glob(
    os.path.join(raw_folder, "*scheme_performance*.csv")
)

if not files:
    raise FileNotFoundError(
        "scheme_performance CSV not found in data/raw"
    )

df = pd.read_csv(files[0])

# Standardise column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("Original columns:", df.columns.tolist())
print("Original records:", len(df))

# Identify return columns
return_cols = [
    col for col in df.columns
    if "return" in col
]

if not return_cols:
    raise ValueError(
        "No return columns found. Check actual column names."
    )

# Convert returns into numeric values
for col in return_cols:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace("%", "", regex=False),
        errors="coerce"
    )

# Identify expense ratio column
expense_candidates = [
    col for col in df.columns
    if "expense_ratio" in col
]

if not expense_candidates:
    raise ValueError(
        "Expense ratio column not found."
    )

expense_col = expense_candidates[0]

df[expense_col] = pd.to_numeric(
    df[expense_col].astype(str).str.replace("%", "", regex=False),
    errors="coerce"
)

# Flag expense ratio anomalies
df["expense_ratio_anomaly"] = (
    (df[expense_col] < 0.1) |
    (df[expense_col] > 2.5) |
    df[expense_col].isna()
)

# Flag extreme returns for review
for col in return_cols:
    df[f"{col}_anomaly"] = (
        df[col].isna() |
        (df[col].abs() > 100)
    )

# Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates()
duplicates_removed = before - len(df)

# Save cleaned dataset
output_file = os.path.join(
    output_folder,
    "clean_performance.csv"
)

df.to_csv(output_file, index=False)

# Final report
print("\n========== PERFORMANCE CLEANING REPORT ==========")

print("Final records:", len(df))
print("Duplicate records removed:", duplicates_removed)

for col in return_cols:
    print(
        f"Invalid {col}:",
        df[col].isna().sum()
    )

print(
    "Expense ratio anomalies:",
    df["expense_ratio_anomaly"].sum()
)

for col in return_cols:
    print(
        f"{col} anomalies:",
        df[f"{col}_anomaly"].sum()
    )

print("\nSaved:", output_file)
print("\nPERFORMANCE CLEANING COMPLETED!")
