import pandas as pd
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_FILE=ROOT_DIR/"data"/"raw"/"olist_sellers_dataset.csv"

df = pd.read_csv(DATA_FILE,dtype={"seller_zip_code_prefix": "string"})

print("SELLERS DATA PROFILING")
print("="*60)

# Dataset dimensions
print("\nDataset shape:",df.shape)

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
print("Duplicate seller IDs:",df["seller_id"].duplicated().sum())

# Blank values
print("\nBlank values:")
for column in df.columns:
    blanks=(df[column].astype("string").str.strip().eq("").sum())
    print(f"{column}:{blanks}")

# Unique sellers and geographic distribution
print("\nUnique sellers:",df["seller_id"].nunique())

print("\nTop 10 states by seller count:")
print(df["seller_state"].value_counts().head(10))

print("\nTop 10 cities by seller count:")
print(df["seller_city"].value_counts().head(10))

# ZIP-prefix format validation
zip_prefix=df["seller_zip_code_prefix"].astype("string").str.strip()
invalid_zip=~zip_prefix.str.fullmatch(r"\d{5}", na=False)
print("\nInvalid ZIP-prefix formats:",int(invalid_zip.sum()))

# State-code format validation
state=df["seller_state"].astype("string").str.strip()
invalid_state=~state.str.fullmatch(r"[A-Za-z]{2}", na=False)
print("Invalid state-code formats:",int(invalid_state.sum()))
