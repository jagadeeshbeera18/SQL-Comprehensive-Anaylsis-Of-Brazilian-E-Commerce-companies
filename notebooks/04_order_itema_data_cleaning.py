import pandas as pd
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
REPORT_DIR = ROOT_DIR / "cleaned_reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")

original_rows = len(df)

# Standardize column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Clean text columns
for column in df.select_dtypes(include=["object", "string"]).columns:
    df[column] = df[column].str.strip()
    df[column] = df[column].replace("", pd.NA)

# Convert numeric columns
numeric_columns = ["order_item_id", "price", "freight_value"]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Convert shipping date
df["shipping_limit_date"] = pd.to_datetime(
    df["shipping_limit_date"],
    errors="coerce"
)

# Validate values
invalid_prices = int((df["price"] <= 0).sum())
invalid_freight = int((df["freight_value"] < 0).sum())

# Check duplicate order-item combinations
duplicate_order_items = int(
    df.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

# Missing values
missing_values = {
    column: int(count)
    for column, count in df.isna().sum().items()
}

# Save cleaned dataset
output_path = PROCESSED_DIR / "clean_order_items.csv"
df.to_csv(output_path, index=False)

# Cleaning report
report = {
    "dataset": "order_items",
    "original_rows": original_rows,
    "processed_rows": len(df),
    "invalid_prices": invalid_prices,
    "invalid_freight_values": invalid_freight,
    "duplicate_order_item_combinations": duplicate_order_items,
    "missing_values": missing_values
}

report_path = REPORT_DIR / "order_items_cleaning_report.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("Order items cleaning completed!")
print("Original rows:", original_rows)
print("Processed rows:", len(df))
print("Invalid prices:", invalid_prices)
print("Invalid freight values:", invalid_freight)
print("Duplicate order-item combinations:", duplicate_order_items)
print("Missing values:", missing_values)
print("Saved:", output_path)