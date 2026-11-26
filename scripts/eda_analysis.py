
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Database connection
conn = sqlite3.connect("bluestock_mf.db")

# Create output folder
os.makedirs("reports/charts", exist_ok=True)

# 1. Investment by age group
age_query = """
SELECT i.age_group,
       SUM(t.amount_inr) AS investment
FROM fact_transactions t
JOIN dim_investor i
ON t.investor_id = i.investor_id
GROUP BY i.age_group
ORDER BY investment DESC
"""

age_df = pd.read_sql_query(age_query, conn)

plt.figure(figsize=(9, 5))
plt.bar(age_df["age_group"], age_df["investment"])
plt.title("Investment by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Investment (INR)")
plt.tight_layout()
plt.savefig("reports/charts/age_group.png")
plt.close()

# 2. Investment by transaction type
type_query = """
SELECT transaction_type,
       SUM(amount_inr) AS investment
FROM fact_transactions
GROUP BY transaction_type
"""

type_df = pd.read_sql_query(type_query, conn)

plt.figure(figsize=(8, 5))
plt.bar(type_df["transaction_type"], type_df["investment"])
plt.title("Investment by Transaction Type")
plt.xlabel("Transaction Type")
plt.ylabel("Investment (INR)")
plt.tight_layout()
plt.savefig("reports/charts/transaction_type.png")
plt.close()

# 3. Investment by city tier
city_query = """
SELECT i.city_tier,
       SUM(t.amount_inr) AS investment
FROM fact_transactions t
JOIN dim_investor i
ON t.investor_id = i.investor_id
GROUP BY i.city_tier
"""

city_df = pd.read_sql_query(city_query, conn)

plt.figure(figsize=(8, 5))
plt.bar(city_df["city_tier"], city_df["investment"])
plt.title("Investment by City Tier")
plt.xlabel("City Tier")
plt.ylabel("Investment (INR)")
plt.tight_layout()
plt.savefig("reports/charts/city_tier.png")
plt.close()

conn.close()

print("EDA ANALYSIS COMPLETED!")
print("Charts saved in reports/charts/")