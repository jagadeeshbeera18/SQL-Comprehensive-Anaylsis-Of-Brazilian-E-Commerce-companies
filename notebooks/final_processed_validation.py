import pandas as pd
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
REPORT_DIR = ROOT_DIR / "cleaned_reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

datasets = {
    "orders": "clean_orders.csv",
    "products": "clean_products.csv",
    "category_names": "clean_category_names.csv",
    "customers": "clean_customers.csv",
    "order_items": "clean_order_items.csv",
    "payments": "clean_payments.csv",
    "sellers": "clean_sellers.csv",
    "reviews": "clean_reviews.csv",
    "geolocation": "clean_geolocation.csv"
}

results = []

print("=" * 60)
print("FINAL PROCESSED DATASET VALIDATION")
print("=" * 60)

for dataset_name, filename in datasets.items():

    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        print(f"\n{dataset_name}: FILE NOT FOUND")

        results.append({
            "dataset": dataset_name,
            "status": "FILE NOT FOUND"
        })
        continue

    df = pd.read_csv(file_path)

    result = {
        "dataset": dataset_name,
        "status": "LOADED",
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": {
            column: int(count)
            for column, count in df.isna().sum().items()
        }
    }

    results.append(result)

    print(f"\nDataset: {dataset_name}")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Duplicate rows:", df.duplicated().sum())
    print("Missing values:", df.isna().sum().sum())

# Save final audit report

report_path = REPORT_DIR / "final_processed_validation.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print("\n" + "=" * 60)
print("FINAL VALIDATION COMPLETED")
print("Report saved:", report_path)
print("=" * 60)