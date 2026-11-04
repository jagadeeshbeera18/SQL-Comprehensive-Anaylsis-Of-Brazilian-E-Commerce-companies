from pathlib import Path
import pandas as pd

ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_PATH=(ROOT_DIR/ "data"/ "raw"/ "product_category_name_translation.csv")

REPORT_DIR=ROOT_DIR/"reports"
REPORT_DIR.mkdir(parents=True,exist_ok=True)
REPORT_PATH = REPORT_DIR /"category_names_profiling_report.txt"

df = pd.read_csv(DATA_PATH)

# Standardize column names
df.columns=df.columns.str.strip().str.lower()

# Remove surrounding whitespace from text columns
for column in df.select_dtypes(include=["object", "string"]).columns:
    df[column]=df[column].str.strip()

print("\n" + "=" * 60)
print("PRODUCT CATEGORY NAMES DATA PROFILING")
print("=" * 60)
print("\nDataset shape:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print("\nColumn names:")
print(df.columns.tolist())
print("\nDataset information:")
df.info()

# Missing-value analysis
print("\n" + "=" * 60)
print("MISSING-VALUE ANALYSIS")
print("=" * 60)

missing_count=df.isna().sum()
missing_report=pd.DataFrame({"missing_count": missing_count,"missing_percentage": (missing_count / len(df) * 100).round(2)})
print(missing_report)

# Duplicate analysis
print("\n" + "=" * 60)
print("DUPLICATE ANALYSIS")
print("=" * 60)
print("Duplicate complete rows:", df.duplicated().sum())
print("Duplicate Portuguese category names:",df["product_category_name"].duplicated().sum())
print("Duplicate English category names:",df["product_category_name_english"].duplicated().sum())

# Blank-value analysis
print("\n" + "=" * 60)
print("BLANK-VALUE ANALYSIS")
print("=" * 60)
for column in df.columns:
    blank_count = (df[column].astype("string").str.strip().eq("").sum())
    print(f"{column}: {blank_count} blank values")

# Translation coverage
print("\n" + "=" * 60)
print("TRANSLATION COVERAGE")
print("=" * 60)
portuguese_categories=df["product_category_name"].nunique()
english_categories=df["product_category_name_english"].nunique()
print("Unique Portuguese categories:", portuguese_categories)
print("Unique English category labels:", english_categories)
print("Rows with missing Portuguese category names:",df["product_category_name"].isna().sum())
print("Rows with missing English translations:",df["product_category_name_english"].isna().sum())

# 8. Investigate duplicate mappings
print("\n" + "=" * 60)
print("DUPLICATE MAPPING INVESTIGATION")
print("=" * 60)
duplicate_portuguese=df[df["product_category_name"].duplicated(keep=False)].sort_values("product_category_name")
duplicate_english=df[df["product_category_name_english"].duplicated(keep=False)].sort_values("product_category_name_english")
print("\nPortuguese categories with multiple rows:")
print(duplicate_portuguese.head(20).to_string(index=False))
print("\nEnglish labels used by multiple rows:")
print(duplicate_english.head(20).to_string(index=False))

# 9. Save profiling reports
with open(REPORT_PATH, "w", encoding="utf-8") as file:
    file.write("PRODUCT CATEGORY NAMES PROFILING REPORT\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Total rows: {len(df)}\n")
    file.write(f"Total columns: {len(df.columns)}\n")
    file.write(
        f"Duplicate complete rows: {df.duplicated().sum()}\n"
    )

    file.write("\nMISSING VALUES\n")
    file.write(missing_report.to_string())

    file.write("\n\nDUPLICATE CATEGORY COUNTS\n")
    file.write(
        f"Duplicate Portuguese names: "
        f"{df['product_category_name'].duplicated().sum()}\n"
    )
    file.write(
        f"Duplicate English labels: "
        f"{df['product_category_name_english'].duplicated().sum()}\n"
    )

    file.write("\n\nDUPLICATE PORTUGUESE MAPPINGS\n")
    file.write(
        duplicate_portuguese.head(50).to_string(index=False)
    )

    file.write("\n\nDUPLICATE ENGLISH LABELS\n")
    file.write(
        duplicate_english.head(50).to_string(index=False)
    )

print("\nCategory names profiling completed.")
print(f"Report saved to: {REPORT_PATH}")