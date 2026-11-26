import sqlite3

conn = sqlite3.connect("bluestock_mf.db")

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
""").fetchall()

for table in tables:
    table_name = table[0]

    print("\n" + "=" * 40)
    print("TABLE:", table_name)
    print("=" * 40)

    columns = conn.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    for column in columns:
        print(column[1], "-", column[2])

conn.close()