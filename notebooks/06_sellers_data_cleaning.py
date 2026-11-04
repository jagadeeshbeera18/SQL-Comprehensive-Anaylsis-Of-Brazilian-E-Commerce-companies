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
df = pd.read_csv(
    RAW_DIR / "olist_sellers_dataset.csv",
    dtype={"seller_zip_code_prefix": "string"}
)

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

# Standardize state codes
df["seller_state"] = df["seller_state"].str.upper()

# Validate ZIP prefix format
zip_valid = df["seller_zip_code_prefix"].str.fullmatch(r"\d{5}")

# Check duplicate seller IDs
duplicate_seller_ids = int(
    df["seller_id"].duplicated().sum()
)

# Missing values
missing_values = {
    column: int(count)
    for column, count in df.isna().sum().items()
}

# Save cleaned dataset
output_path = PROCESSED_DIR / "clean_sellers.csv"
df.to_csv(output_path, index=False)

# Cleaning report
report = {
    "dataset": "sellers",
    "original_rows": original_rows,
    "processed_rows": len(df),
    "duplicate_seller_ids": duplicate_seller_ids,
    "invalid_zip_prefixes": int((~zip_valid.fillna(False)).sum()),
    "missing_values": missing_values
}

report_path = REPORT_DIR / "sellers_cleaning_report.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("Sellers cleaning completed!")
print("Original rows:", original_rows)
print("Processed rows:", len(df))
print("Duplicate seller IDs:", duplicate_seller_ids)
print("Invalid ZIP prefixes:", report["invalid_zip_prefixes"])
print("Missing values:", missing_values)
print("Saved:", output_path)