import pandas as pd
import mysql.connector
from pathlib import Path


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ravi@123',
    'database': 'stock_analysis_db'
}

# Connect to database
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()
print("✅ Connected to database")

# Clear old data
cursor.execute("DELETE FROM stock_prices_clean")
conn.commit()

# Load CSV files
data_folder = Path(r"C:\stock analysis\data_csv")
total = 0

for csv_file in data_folder.glob("*.csv"):
    df = pd.read_csv(csv_file)
    
    # Handle Ticker vs symbol
    if "Ticker" in df.columns:
        df["symbol"] = df["Ticker"]
    
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["daily_return"] = df["close"].pct_change()
    df["year"] = df["date"].dt.year
    df["month_name"] = df["date"].dt.strftime("%B")
    
    # Replace NaN with None for SQL
    df = df.where(pd.notna(df), None)
    
    for _, row in df.iterrows():
        # Build parameters and sanitize NaN values to Python None so the
        # MySQL driver sends SQL NULL instead of the literal 'nan'. Also
        # convert pandas Timestamp to native python datetime when present.
        def clean(val):
            if pd.isna(val):
                return None
            # Convert Timestamp to python datetime
            if hasattr(val, 'to_pydatetime'):
                return val.to_pydatetime()
            return val

        params = (
            clean(row.get("symbol")),
            clean(row.get("date")),
            clean(row.get("open")),
            clean(row.get("high")),
            clean(row.get("low")),
            clean(row.get("close")),
            clean(row.get("volume")),
            clean(row.get("daily_return")),
            clean(row.get("year")),
            clean(row.get("month_name")),
        )

        cursor.execute("""
            INSERT INTO stock_prices_clean 
            (symbol, trade_date, open_price, high_price, low_price, close_price, 
             volume, daily_return, year, month_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, params)
        total += 1
    
    print(f"✓ {csv_file.name}")

conn.commit()
print(f"\n✅ Loaded {total} records!")

# Add sectors
sectors = {
    'RELIANCE': 'Energy', 'TCS': 'IT', 'HDFCBANK': 'Banking', 'INFY': 'IT',
    'ICICIBANK': 'Banking', 'HINDUNILVR': 'FMCG', 'ITC': 'FMCG', 'SBIN': 'Banking',
    'BHARTIARTL': 'Telecom', 'WIPRO': 'IT', 'MARUTI': 'Automobile', 'TATAMOTORS': 'Automobile'
}

cursor.execute("DELETE FROM stock_sector_map")
for symbol, sector in sectors.items():
    cursor.execute("INSERT INTO stock_sector_map VALUES (%s, %s)", (symbol, sector))
conn.commit()

# Calculate metrics
cursor.execute("DELETE FROM stock_metrics_yearly")
cursor.execute("""
    INSERT INTO stock_metrics_yearly 
    SELECT symbol, year, 
           (MAX(close_price)-MIN(close_price))/MIN(close_price),
           STD(daily_return)*SQRT(252), AVG(close_price), AVG(volume)
    FROM stock_prices_clean WHERE daily_return IS NOT NULL
    GROUP BY symbol, year
""")
conn.commit()

cursor.close()
conn.close()
print("🎉 Done!")
