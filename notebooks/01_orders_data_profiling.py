import pandas as pd
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_FILE=(ROOT_DIR/"data"/"raw"/"olist_orders_dataset.csv")
df=pd.read_csv(DATA_FILE)

print('\n--- FIRST FIVE ROWS ---')
print(df.head())
print("\n--- DATASET SHAPE ---")
print(f"ROWS:{df.shape[0]}")
print(f"COLUMNS:{df.shape[1]}")
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())
print("\n--- DATASET INFORMATION ---")
print(df.info())

print("\n--- STATISTICAL SUMMARY ---")
print(df.describe(include="all").T)

print("\n--- MISSING VALUES ---")
missing=df.isna().sum()
missing_report=pd.DataFrame({"missing_count":missing,"missing_percentage":(missing/len(df)*100).round(2)})
print(missing_report[missing_report["missing_count"]>0].sort_values("missing_count",ascending=False))

print("\n--- DUPLICATE RECORDS ---")
print(f"Complete Duplicate rows:{df.duplicated().sum()}")
print("Duplicate order IDs:",df['order_id'].duplicated().sum())

print("\n--- ORDER STATUS DISTRIBUTION ---")
print(df['order_status'].value_counts(dropna=False))

