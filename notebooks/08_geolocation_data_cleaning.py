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
    RAW_DIR / "olist_geolocation_dataset.csv",
    dtype={"geolocation_zip_code_prefix": "string"}
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

# FIXED: Pad ZIP code prefix to 5 digits to restore leading zeros lost in CSV export
df["geolocation_zip_code_prefix"] = (
    df["geolocation_zip_code_prefix"].str.zfill(5)
)

# Standardize state codes
df["geolocation_state"] = (
    df["geolocation_state"].str.upper()
)

# Convert coordinates to numeric
coordinate_columns = [
    "geolocation_lat",
    "geolocation_lng"
]

for column in coordinate_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Validate ZIP prefix format
zip_valid = df["geolocation_zip_code_prefix"].str.fullmatch(
    r"\d{5}"
)

# Validate latitude and longitude ranges
invalid_latitude = int(
    (~df["geolocation_lat"].between(-90, 90)).sum()
)

invalid_longitude = int(
    (~df["geolocation_lng"].between(-180, 180)).sum()
)

# Count exact duplicate records
duplicate_rows = int(df.duplicated().sum())

# Count unique ZIP prefixes
unique_zip_prefixes = int(
    df["geolocation_zip_code_prefix"].nunique()
)

# Missing values
missing_values = {
    column: int(count)
    for column, count in df.isna().sum().items()
}

# Save cleaned dataset
output_path = PROCESSED_DIR / "clean_geolocation.csv"
df.to_csv(output_path, index=False)

# Generate cleaning report
report = {
    "dataset": "geolocation",
    "original_rows": original_rows,
    "processed_rows": len(df),
    "duplicate_rows": duplicate_rows,
    "unique_zip_prefixes": unique_zip_prefixes,
    "invalid_zip_prefixes": int((~zip_valid.fillna(False)).sum()),
    "invalid_latitudes": invalid_latitude,
    "invalid_longitudes": invalid_longitude,
    "missing_values": missing_values
}

report_path = REPORT_DIR / "geolocation_cleaning_report.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("Geolocation cleaning completed!")
print("Original rows:", original_rows)
print("Processed rows:", len(df))
print("Duplicate rows:", duplicate_rows)
print("Unique ZIP prefixes:", unique_zip_prefixes)
print("Invalid ZIP prefixes:", report["invalid_zip_prefixes"])
print("Invalid latitudes:", invalid_latitude)
print("Invalid longitudes:", invalid_longitude)
print("Missing values:", missing_values)
print("Saved:", output_path)