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
    RAW_DIR / "olist_order_payments_dataset.csv"
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

# Standardize payment type
df["payment_type"] = df["payment_type"].str.lower()

# Convert numeric columns
numeric_columns = [
    "payment_sequential",
    "payment_installments",
    "payment_value"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Validate payment values
zero_payments = int((df["payment_value"] == 0).sum())
negative_payments = int((df["payment_value"] < 0).sum())

invalid_installments = int(
    (df["payment_installments"] <= 0).sum()
)

# Check duplicate payment records
duplicate_payments = int(
    df.duplicated(
        subset=["order_id", "payment_sequential"]
    ).sum()
)

# Missing values
missing_values = {
    column: int(count)
    for column, count in df.isna().sum().items()
}

# Payment type distribution
payment_type_distribution = {
    str(key): int(value)
    for key, value in df["payment_type"]
    .value_counts(dropna=False).items()
}

# Save cleaned dataset
output_path = PROCESSED_DIR / "clean_payments.csv"
df.to_csv(output_path, index=False)

# Generate cleaning report
report = {
    "dataset": "payments",
    "original_rows": original_rows,
    "processed_rows": len(df),
    "zero_payment_values": zero_payments,
    "negative_payment_values": negative_payments,
    "invalid_installments": invalid_installments,
    "duplicate_payment_records": duplicate_payments,
    "missing_values": missing_values,
    "payment_type_distribution": payment_type_distribution
}

report_path = REPORT_DIR / "payments_cleaning_report.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("Payments cleaning completed!")
print("Original rows:", original_rows)
print("Processed rows:", len(df))
print("Zero payments:", zero_payments)
print("Negative payments:", negative_payments)
print("Invalid installments:", invalid_installments)
print("Duplicate payment records:", duplicate_payments)
print("Payment types:", payment_type_distribution)
print("Missing values:", missing_values)
print("Saved:", output_path)