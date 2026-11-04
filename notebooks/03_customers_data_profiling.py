import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE=ROOT_DIR/"data"/"raw"/"olist_customers_dataset.csv"

df=pd.read_csv(DATA_FILE,dtype={"customer_zip_code_prefix":"string","customer_state":"string",})

print("PRODUCT DATASET PROFILE")
print("="*60)

print('\n--- FIRST FIVE ROWS ---')
print(df.head())
print("\n--- DATASET SHAPE ---")
print(f"ROWS:{df.shape[0]}")
print(f"COLUMNS:{df.shape[1]}")
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())
print("\n--- DATASET INFORMATION ---")
print(df.info())
print("\nMissing values:")
missing=df.isnull().sum()
print(missing[missing > 0] if missing.sum() else "No missing values")

print("\nDuplicate Rows:",int(df.duplicated().sum()))
print("Duplicate customer IDs:",int(df['customer_id'].duplicated().sum()))

# Customer distribution by state
print("\nCustomers by state:")
print(df["customer_state"].value_counts(dropna=False).head(10))

# Invalid zip codes
zip_prefix=df["customer_zip_code_prefix"]
invalid_zip=(zip_prefix.isna()| ~zip_prefix.str.fullmatch(r"\d{5}", na=False))
print("\nInvalid ZIP-prefix formats:",int(invalid_zip.sum()))

# Invalid customer states
state=df["customer_state"]
invalid_state=(state.isna()| ~state.str.fullmatch(r"[A-Z]{2}", na=False))
print("Invalid state-code formats:",int(invalid_state.sum()))

# Number of unique customer identifiers
print("\nUnique customer IDs:",df["customer_id"].nunique())

# Number of unique customer-location IDs
print("Unique customer_unique_id values:",df["customer_unique_id"].nunique())
print("\nCustomer profiling completed.")