import pandas as pd
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_FILE=ROOT_DIR/"data"/"raw"/"olist_order_reviews_dataset.csv"

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

print("Duplicate review IDs:",df["review_id"].duplicated().sum())

# Review score distribution
print("\nReview score counts:")
print(df["review_score"].value_counts().sort_index())

print("\nReview score percentages:")
print(df["review_score"].value_counts(normalize=True).sort_index().mul(100).round(2))

print("\nAverage review score:",round(df["review_score"].mean(),2))
print("Median review score:",df["review_score"].median())

# Validate review scores
invalid_scores=~df["review_score"].isin([1, 2, 3, 4, 5])

print("\nInvalid review scores:", int(invalid_scores.sum()))

# Date conversion
date_columns = ["review_creation_date","review_answer_timestamp"]
for column in date_columns:
    df[column]=pd.to_datetime(df[column], errors="coerce")

print("\nMissing or invalid review dates:")
for column in date_columns:
    print(f"{column}:{df[column].isna().sum()}")

# Check answers submitted before review creation
invalid_date_order = (df["review_answer_timestamp"].notna()& df["review_creation_date"].notna()
                    &( df["review_answer_timestamp"]< df["review_creation_date"]))
print("\nAnswers before review creation:",int(invalid_date_order.sum()))

# Review ID and order ID relationship
print("\nUnique review IDs:",df["review_id"].nunique())
print("Unique order IDs:",df["order_id"].nunique())

reviews_per_order=df.groupby("order_id").size()

print("\nReviews per order:")
print(reviews_per_order.describe())
