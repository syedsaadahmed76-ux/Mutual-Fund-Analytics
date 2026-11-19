
import pandas as pd
import os

# Dataset location
DATA_FOLDER = "data/raw"

# Find all CSV files
csv_files = [
    file for file in os.listdir(DATA_FOLDER)
    if file.lower().endswith(".csv")
]

print("Total CSV files:", len(csv_files))

# Load datasets
datasets = {}

for file in csv_files:

    file_path = os.path.join(DATA_FOLDER, file)

    print("\n" + "=" * 60)
    print("DATASET:", file)
    print("=" * 60)

    df = pd.read_csv(file_path)

    datasets[file] = df

    # Dataset shape
    print("\nShape:")
    print(df.shape)

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # First five rows
    print("\nFirst 5 Rows:")
    print(df.head())

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Duplicate rows
    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

print("\nAll datasets loaded successfully!")
