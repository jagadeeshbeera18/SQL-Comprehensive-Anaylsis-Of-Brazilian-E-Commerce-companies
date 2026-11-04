import pandas as pd
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_FILE=ROOT_DIR/"data"/"raw"/"olist_geolocation_dataset.csv"

df=pd.read_csv(DATA_FILE)

print("REVIEWS DATA PROFILING")
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

print("unique ZIP perfixes:",df['geolocation_zip_code_prefix'].nunique())
print("unique coordinates:",df[['geolocation_lat','geolocation_lng']].drop_duplicates().shape[0])

# state Disctribution
print("\n"+"="*60)
print("Records by state")
print("\n"+"="*60)
print(df['geolocation_state'].value_counts(dropna=False).head(15))

# city Distribution
print("\n"+"="*60)
print("Records by state")
print("\n"+"="*60)
print(df['geolocation_city'].value_counts(dropna=False).head(15))

print("\n"+"="*60)
print("Geographic Coverage")
print("\n"+"="*60)
print("unique states:",df['geolocation_state'].nunique())
print("unique city labels:",df['geolocation_city'].nunique())
print("unique zip prefixes:",df['geolocation_zip_code_prefix'].nunique())