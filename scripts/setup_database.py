import sqlite3
import pandas as pd

df = pd.read_csv("data/sales.csv")

# ✅ Convert to proper datetime
df['order_date'] = pd.to_datetime(df['order_date'], format='%d-%m-%Y')

conn = sqlite3.connect("database/sales.db")

df.to_sql("sales", conn, if_exists="replace", index=False)

print("Database created!")

conn.close()