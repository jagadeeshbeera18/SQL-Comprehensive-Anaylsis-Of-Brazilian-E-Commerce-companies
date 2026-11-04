import pandas as pd
import json
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]

DATA_FILE=ROOT_DIR/"data"/"raw"/"olist_orders_dataset.csv"
OUTPUT_DIR=ROOT_DIR/"data"/"processed"
REPORT_DIR=ROOT_DIR/"cleaned_reports"

OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
REPORT_DIR.mkdir(parents=True,exist_ok=True)

# 1. Load dataset
df=pd.read_csv(DATA_FILE)
original_rows=len(df)

print("Original shape:",df.shape)

# 2. Standardize column names
df.columns=df.columns.str.strip().str.lower()

# 3. Remove leading/trailing whitespace
text_columns=df.select_dtypes(include=["object", "string"]).columns
for column in text_columns:
    df[column] = df[column].str.strip()

# 4. Convert timestamp columns to datetime
date_columns=["order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]
for column in date_columns:
    df[column]=pd.to_datetime(df[column],errors="coerce")

# 6. Flag suspicious delivery records
df["delivery_date_quality_issue"]=((df["order_status"]=="delivered") & df["order_delivered_customer_date"].isna())
df["carrier_date_quality_issue"]=((df["order_status"]=="delivered")& df["order_delivered_carrier_date"].isna())
print("\nDelivery Data Quality Summary")
print("=" * 60)
print("Delivered orders missing customer delivery date:",int(df["delivery_date_quality_issue"].sum()))
print("Delivered orders missing carrier handover date:",int(df["carrier_date_quality_issue"].sum()))

# 7. Analyze missing dates by order status
analysis_columns=["order_approved_at","order_delivered_carrier_date","order_delivered_customer_date"]
missing_by_status=(df.groupby("order_status")[analysis_columns].agg(lambda column: column.isna().sum()))
print("\nMissing Dates by Order Status")
print("=" * 60)
print(missing_by_status)

missing_percentage=(df.groupby("order_status")[analysis_columns].agg(lambda column: column.isna().mean() * 100).round(2))
print("\nMissing Date Percentages by Order Status")
print("=" * 60)
print(missing_percentage)

# 8. Investigate delivered orders missing delivery dates
affected_orders = df[(df["order_status"] == "delivered") & df["order_delivered_customer_date"].isna()].copy()
investigation_columns = [
    "order_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

print("\nAffected Delivered Orders")
print("=" * 60)
print(affected_orders[investigation_columns].to_string(index=False))

print("\nMissing Values in Affected Orders")
print(affected_orders[investigation_columns].isna().sum())

# 9. Save processed data
output_file = OUTPUT_DIR / "clean_orders.csv"
df.to_csv(output_file, index=False)

# 10. Generate a cleaning report
report={
    "dataset": "olist_orders_dataset.csv",
    "original_rows": original_rows,
    "rows_after_cleaning": len(df),
    "delivered_missing_customer_delivery_date": int(df["delivery_date_quality_issue"].sum()),
    "delivered_missing_carrier_date": int(df["carrier_date_quality_issue"].sum()),
    "missing_values_after_processing": {
        column: int(count)
        for column, count in df.isna().sum().items()
        if count > 0
    },
    "output_file": str(output_file),
}

report_file=REPORT_DIR / "orders_cleaning_report.json"

with open(report_file, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("\nProcessing Completed")
print("=" * 60)
print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Processed dataset:", output_file)
print("Cleaning report:", report_file)
