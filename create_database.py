
import sqlite3
import os

db_path = "bluestock_mf.db"

if not os.path.exists(db_path):
    print("Database file not found!")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
    """)

    print("\nDATABASE TABLES")

    for row in cursor.fetchall():
        print(row[0])

    conn.close()
    print("\nDatabase connection successful!")
