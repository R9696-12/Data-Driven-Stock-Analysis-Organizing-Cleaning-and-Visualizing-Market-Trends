import os
import yaml
import pandas as pd

RAW_FOLDER = r"C:\stock analysis\data"
OUTPUT_FOLDER = r"C:\stock analysis\data_csv"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# dictionary to store data per symbol
symbol_data = {}

for month in os.listdir(RAW_FOLDER):
    month_path = os.path.join(RAW_FOLDER, month)

    if not os.path.isdir(month_path):
        continue

    for file in os.listdir(month_path):
        if file.endswith(".yaml") or file.endswith(".yml"):
            file_path = os.path.join(month_path, file)

            with open(file_path, "r") as f:
                data = yaml.safe_load(f)

            for entry in data:
                symbol = entry.get("symbol") or entry.get("Ticker")

                if symbol is None:
                    print("Skipping entry (missing symbol/Ticker):", entry)
                    continue

                if symbol not in symbol_data:
                    symbol_data[symbol] = []

                symbol_data[symbol].append(entry)

# save each symbol to individual CSV
for symbol, rows in symbol_data.items():
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUTPUT_FOLDER}/{symbol}.csv", index=False)

print("Extraction Completed. CSV files are ready.")
