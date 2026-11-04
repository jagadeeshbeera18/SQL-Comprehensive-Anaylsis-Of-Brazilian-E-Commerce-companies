import pandas as pd
import json
from pathlib import Path

# Project paths
ROOT_DIR=Path(__file__).resolve().parents[1]
RAW_DIR=ROOT_DIR/"data"/"raw"
PROCESSED_DIR=ROOT_DIR/"data"/"processed"
REPORT_DIR=ROOT_DIR/"cleaned_reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(
    RAW_DIR / "olist_customers_dataset.csv",
    dtype={"customer_zip_code_prefix": "string"}
)

original_rows = len(df)

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Remove whitespace from text columns
for column in df.select_dtypes(include=["object", "string"]).columns:
    df[column] = df[column].str.strip()
    df[column] = df[column].replace("", pd.NA)

# Standardize state codes
df["customer_state"] = df["customer_state"].str.upper()

# Validate ZIP prefix format without changing original values
zip_valid = df["customer_zip_code_prefix"].str.fullmatch(r"\d{5}")

# Check duplicate IDs
duplicate_customer_ids = int(
    df["customer_id"].duplicated().sum()
)

# Check missing values
missing_values = {
    column: int(count)
    for column, count in df.isna().sum().items()
}

# Save cleaned dataset
output_path = PROCESSED_DIR / "clean_customers.csv"
df.to_csv(output_path, index=False)

# Generate report
report = {
    "dataset": "customers",
    "original_rows": original_rows,
    "processed_rows": len(df),
    "duplicate_customer_ids": duplicate_customer_ids,
    "invalid_zip_prefixes": int((~zip_valid.fillna(False)).sum()),
    "missing_values": missing_values
}

report_path = REPORT_DIR / "customers_cleaning_report.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("Customer cleaning completed!")
print("Original rows:", original_rows)
print("Processed rows:", len(df))
print("Duplicate customer IDs:", duplicate_customer_ids)
print("Invalid ZIP prefixes:", report["invalid_zip_prefixes"])
print("Missing values:", missing_values)
print("Saved:", output_path)