import os
import pandas as pd
import matplotlib.pyplot as plt

CSV_DIR = r"C:\stock analysis\data_csv"

def load_all_stocks():
    all_data = []

    for file in os.listdir(CSV_DIR):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(CSV_DIR, file))
            df["symbol"] = file.replace(".csv", "")
            df["date"] = pd.to_datetime(df["date"])
            df["daily_return"] = df["close"].pct_change()
            all_data.append(df)

    return pd.concat(all_data)

df = load_all_stocks()


# 2. VOLATILITY ANALYSIS (Std Dev of Daily Returns)
volatility = df.groupby("symbol")["daily_return"].std()
top10_volatility = volatility.sort_values(ascending=False).head(10)
print("\n==== TOP 10 MOST VOLATILE STOCKS ====")
print(top10_volatility)

plt.figure(figsize=(10, 5))
top10_volatility.plot(kind="bar")
plt.title("Top 10 Most Volatile Stocks")
plt.xlabel("Stock Symbol")
plt.ylabel("Volatility")
plt.tight_layout()
plt.show()

# 3. CUMULATIVE RETURN OVER TIME
df["cumulative_return"] = (1 + df["daily_return"]).groupby(df["symbol"]).cumprod()

# Top 5 best stocks based on total growth
yearly = df.groupby("symbol")["cumulative_return"].last()
top5 = yearly.sort_values(ascending=False).head(5).index

plt.figure(figsize=(12, 6))
for symbol in top5:
    stock_df = df[df["symbol"] == symbol]
    plt.plot(stock_df["date"], stock_df["cumulative_return"], label=symbol)

plt.title("Cumulative Return Over Time (Top 5 Stocks)")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.tight_layout()
plt.show()

# 4. SECTOR-WISE PERFORMANCE

SECTOR_FILE = r"C:\stock analysis\sector.csv"

if os.path.exists(SECTOR_FILE):
    sector_map = pd.read_csv(SECTOR_FILE)

    yearly_returns = df.groupby("symbol")["close"].agg(["first", "last"])
    yearly_returns["yearly_return"] = (yearly_returns["last"] - yearly_returns["first"]) / yearly_returns["first"]
    yearly_returns = yearly_returns.reset_index()

    merged = yearly_returns.merge(sector_map, on="symbol")
    sector_avg = merged.groupby("sector")["yearly_return"].mean()

    print("\n==== SECTOR-WISE PERFORMANCE ====")
    print(sector_avg)

    plt.figure(figsize=(10, 5))
    sector_avg.plot(kind="bar")
    plt.title("Average Yearly Return by Sector")
    plt.xlabel("Sector")
    plt.ylabel("Avg Yearly Return")
    plt.tight_layout()
    plt.show()
else:
    print("\nSector file not found → Skipping sector-wise performance.")

# 5. STOCK PRICE CORRELATION HEATMAP

pivot = df.pivot_table(index="date", columns="symbol", values="close")
corr_matrix = pivot.corr()

plt.figure(figsize=(12, 10))
plt.imshow(corr_matrix, cmap="coolwarm")
plt.colorbar()
plt.title("Stock Price Correlation Heatmap")
plt.xticks(range(len(corr_matrix)), corr_matrix.columns, rotation=90)
plt.yticks(range(len(corr_matrix)), corr_matrix.columns)
plt.tight_layout()
plt.show()

# 6. MONTH-WISE TOP 5 GAINERS AND LOSERS
df["month"] = df["date"].dt.to_period("M")

monthly = df.groupby(["symbol", "month"])["close"].agg(["first", "last"])
monthly["monthly_return"] = (monthly["last"] - monthly["first"]) / monthly["first"]

monthly = monthly.reset_index()

print("\n==== MONTH-WISE TOP 5 GAINERS & LOSERS ====\n")

months = monthly["month"].unique()

for m in months:
    print(f"\n--------- {m} ---------")
    month_df = monthly[monthly["month"] == m]

    sorted_df = month_df.sort_values("monthly_return", ascending=False)

    print("\nTop 5 Gainers:")
    print(sorted_df.head(5)[["symbol", "monthly_return"]])

    print("\nTop 5 Losers:")
    print(sorted_df.tail(5)[["symbol", "monthly_return"]])
