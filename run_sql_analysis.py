import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("bluestock_mf.db")

# Read SQL queries
with open("sql/queries.sql", "r", encoding="utf-8") as file:
    sql_script = file.read()

# Execute each query separately
queries = sql_script.split(";")

for i, query in enumerate(queries, start=1):

    query = query.strip()

    if not query:
        continue

    if query.startswith("--"):
        # Remove SQL comments
        query = "\n".join(
            line for line in query.splitlines()
            if not line.strip().startswith("--")
        ).strip()

    if not query:
        continue

    print("\n" + "=" * 60)
    print(f"QUERY {i}")
    print("=" * 60)

    try:
        result = pd.read_sql_query(query, conn)
        print(result.to_string(index=False))

    except Exception as e:
        print("Error:", e)

conn.close()

print("\nALL SQL QUERIES EXECUTED!")