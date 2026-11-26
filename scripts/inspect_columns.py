
import pandas as pd
import glob
import os

files = glob.glob("data/processed/*.csv")

os.makedirs("reports", exist_ok=True)

with open("reports/column_details.txt", "w", encoding="utf-8") as report:

    for file in files:
        df = pd.read_csv(file, nrows=5)

        report.write("\n" + "=" * 60 + "\n")
        report.write(f"FILE: {os.path.basename(file)}\n")
        report.write("=" * 60 + "\n")

        report.write("\nCOLUMN NAMES:\n")

        for col in df.columns:
            report.write(f"- {col}\n")

        report.write("\nDATA TYPES:\n")
        report.write(df.dtypes.to_string())

        report.write("\n\nFIRST 2 RECORDS:\n")
        report.write(df.head(2).to_string(index=False))
        report.write("\n")

print("COLUMN INSPECTION COMPLETED!")
print("Saved: reports/column_details.txt")
