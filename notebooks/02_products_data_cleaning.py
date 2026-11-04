import pandas as pd
import json
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]

DATA_FILE=ROOT_DIR/ "data"/"raw"/"olist_products_dataset.csv"
OUTPUT_DIR = ROOT_DIR/"data"/"processed"
REPORT_DIR = ROOT_DIR/"cleaned_reports"

OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
REPORT_DIR.mkdir(parents=True,exist_ok=True)

# Load raw data
df=pd.read_csv(DATA_FILE)
original_rows=len(df)
print("Original dataset shape:",df.shape)

# Standardize column names
df.columns=df.columns.str.strip().str.lower()

# Remove whitespace from text columns
text_columns=df.select_dtypes(include=["object", "string"]).columns

for column in text_columns:
    df[column]=df[column].str.strip()

# Convert numeric columns safely
numeric_columns = ["product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    ]

for column in numeric_columns:
    df[column]=pd.to_numeric(df[column], errors="coerce")

# Identify quality issues without deleting records
catalog_columns=["product_category_name","product_name_lenght","product_description_lenght","product_photos_qty"]
missing_catalog_mask=df[catalog_columns].isna().all(axis=1)

# Check for duplicate product IDs
duplicate_product_ids=int(df["product_id"].duplicated().sum())

# Check for missing product IDs
missing_product_ids=int(df["product_id"].isna().sum())

# Flag invalid physical measurements
measurement_columns=["product_weight_g","product_length_cm","product_height_cm","product_width_cm",]
invalid_measurements={}
for column in measurement_columns:
    invalid_measurements[column]=int((df[column] < 0).sum())

# Save processed dataset
output_file=OUTPUT_DIR/"clean_products.csv"
df.to_csv(output_file,index=False)

# Save a cleaning report
report = {
    "dataset": "olist_products_dataset.csv",
    "original_rows": int(original_rows),
    "final_rows": int(len(df)),
    "rows_removed": int(original_rows - len(df)),
    "products_missing_all_catalog_attributes": int(
        missing_catalog_mask.sum()
    ),
    "duplicate_product_ids": duplicate_product_ids,
    "missing_product_ids": missing_product_ids,
    "negative_measurement_counts": invalid_measurements,
    "missing_values_after_processing": {
        column: int(count)
        for column,count in df.isna().sum().items()
        if count > 0
    },
}

report_file=REPORT_DIR/"products_cleaning_report.json"

with open(report_file, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("\nProduct Cleaning Completed")
print("=" * 45)
print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))
print(
    "Products missing all catalog attributes:",
    int(missing_catalog_mask.sum())
)
print("Duplicate product IDs:", duplicate_product_ids)
print("Missing product IDs:", missing_product_ids)
print("Processed file:", output_file)
print("Cleaning report:", report_file)