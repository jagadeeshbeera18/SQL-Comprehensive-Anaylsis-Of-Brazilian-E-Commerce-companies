import pandas as pd
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_FILE=ROOT_DIR / "data" / "raw" / "olist_order_items_dataset.csv"

df=pd.read_csv(DATA_FILE)

print("ORDER ITEMS DATA PROFILING")
print("="*60)

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
print(missing[missing>0] if missing.sum() else "No missing values")

# Duplicate records
print("\nDuplicate complete rows:",df.duplicated().sum())

# Duplicate order-item combinations
print("Duplicate order_id + order_item_id combinations:",df.duplicated(subset=["order_id", "order_item_id"]).sum())

# Unique counts
print("\nUnique orders:",df["order_id"].nunique())
print("Unique products:",df["product_id"].nunique())
print("Unique sellers:",df["seller_id"].nunique())

# Price and freight analysis
print("\nPrice statistics:")
print(df["price"].describe())

print("\nFreight value statistics:")
print(df["freight_value"].describe())

# Potentially invalid numeric values
print("\nZero or negative item prices:", (df["price"] <= 0).sum())
print("Negative freight values:", (df["freight_value"] < 0).sum())

# 9. Order items per order
items_per_order=df.groupby("order_id").size()

print("\nOrder items per order:")
print(items_per_order.describe())
print("\nMost frequent order-item counts:")
print(items_per_order.value_counts().sort_index().head(10))
