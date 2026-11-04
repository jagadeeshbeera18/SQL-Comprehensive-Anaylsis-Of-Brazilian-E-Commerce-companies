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
    RAW_DIR / "olist_order_reviews_dataset.csv"
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

# Convert review score
df["review_score"] = pd.to_numeric(
    df["review_score"],
    errors="coerce"
)

# Convert review timestamps
date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )

# Validate review scores
invalid_scores = int(
    (~df["review_score"].between(1, 5)).sum()
)

# Check duplicate review IDs
duplicate_review_ids = int(
    df["review_id"].duplicated().sum()
)

# Check duplicate review-order combinations
duplicate_review_orders = int(
    df.duplicated(
        subset=["review_id", "order_id"]
    ).sum()
)

# Missing values
missing_values = {
    column: int(count)
    for column, count in df.isna().sum().items()
}

# Review score distribution
score_distribution = {
    str(key): int(value)
    for key, value in df["review_score"]
    .value_counts(dropna=False).items()
}

# Save cleaned dataset
output_path = PROCESSED_DIR / "clean_reviews.csv"
df.to_csv(output_path, index=False)

# Generate cleaning report
report = {
    "dataset": "reviews",
    "original_rows": original_rows,
    "processed_rows": len(df),
    "invalid_review_scores": invalid_scores,
    "duplicate_review_ids": duplicate_review_ids,
    "duplicate_review_order_combinations": duplicate_review_orders,
    "missing_values": missing_values,
    "review_score_distribution": score_distribution
}

report_path = REPORT_DIR / "reviews_cleaning_report.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("Reviews cleaning completed!")
print("Original rows:", original_rows)
print("Processed rows:", len(df))
print("Invalid review scores:", invalid_scores)
print("Duplicate review IDs:", duplicate_review_ids)
print("Duplicate review-order combinations:", duplicate_review_orders)
print("Review score distribution:", score_distribution)
print("Missing values:", missing_values)
print("Saved:", output_path)