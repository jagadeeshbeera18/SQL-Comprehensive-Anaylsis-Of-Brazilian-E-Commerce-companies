import pandas as pd
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_FILE=ROOT_DIR/"data"/"raw"/"olist_order_payments_dataset.csv"

df = pd.read_csv(DATA_FILE)

print("PAYMENTS DATA PROFILING")
print("=" * 60)

# Dataset dimensions
print("\nDataset shape:", df.shape)

# Column names and data types
print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset information:")
df.info()

# Missing values
print("\nMissing values:")
missing=df.isnull().sum()
print(missing[missing > 0] if missing.sum() else "No missing values")

# Duplicate records
print("\nDuplicate complete rows:", df.duplicated().sum())

# Check duplicate order-payment combinations
print("Duplicate order_id + payment_sequential combinations:",df.duplicated(subset=["order_id","payment_sequential"]).sum())

# Unique counts
print("\nUnique orders:", df["order_id"].nunique())

print("\nPayment methods:")
print(df["payment_type"].value_counts(dropna=False))

# Payment value statistics
print("\nPayment value statistics:")
print(df["payment_value"].describe())

# Payment installment statistics
print("\nPayment installment statistics:")
print(df["payment_installments"].describe())

# Potentially invalid values
print("\nZero payment values:",(df["payment_value"] == 0).sum())
print("Negative payment values:",(df["payment_value"] < 0).sum())
print("\nZero installment values:",(df["payment_installments"] == 0).sum())
print("Negative installment values:",(df["payment_installments"] < 0).sum())

# Payment method distribution
print("\nPayment method percentages:")
payment_percentages=(df["payment_type"].value_counts(normalize=True,dropna=False)*100).round(2)
print(payment_percentages)

# Orders with multiple payment records
payments_per_order=df.groupby("order_id").size()
print("\nPayment records per order:")
print(payments_per_order.describe())
print("\nMost frequent payment-record counts:")
print(payments_per_order.value_counts().sort_index().head(10))
