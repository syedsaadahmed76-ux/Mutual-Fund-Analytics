
import pandas as pd
import glob
import os

files = glob.glob("data/processed/*.csv")

report = []

for file in files:
    df = pd.read_csv(file)

    report.append("\n" + "=" * 60)
    report.append(f"FILE: {os.path.basename(file)}")
    report.append(f"ROWS: {len(df)}")
    report.append(f"COLUMNS: {len(df.columns)}")
    report.append(f"COLUMN NAMES: {df.columns.tolist()}")
    report.append("\nDATA TYPES:")
    report.append(df.dtypes.to_string())
    report.append("\nFIRST 2 RECORDS:")
    report.append(df.head(2).to_string(index=False))

    print(f"Inspected: {os.path.basename(file)}")

output = "\n".join(report)

os.makedirs("reports", exist_ok=True)

with open("reports/dataset_inspection.txt", "w", encoding="utf-8") as f:
    f.write(output)

print("\nInspection completed!")
print("Report saved: reports/dataset_inspection.txt")
