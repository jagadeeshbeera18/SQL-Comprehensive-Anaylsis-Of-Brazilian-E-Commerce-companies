import json
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"

REPORT_FILES = [
    "orders_validation_report.json",
    "products_validation_report.json",
    "customers_validation_report.json",
    "order_items_validation_report.json",
    "payments_validation_report.json",
    "sellers_validation_report.json",
    "order_reviews_validation_report.json",
    "order_geolocation_validation_report.json",
    "category_names_validation_report.json",
]

def load_report(report_path):
    with open(report_path, "r", encoding="utf-8") as file:
        return json.load(file)

def extract_quality_metrics(report, filename):
    missing_values = report.get("missing_values", {})
    total_missing = sum(missing_values.values())
    total_rows = report.get("total_rows", 0)
    duplicate_rows = report.get("duplicate_complete_rows", 0)
    
    if total_rows:
        duplicate_percentage = round(duplicate_rows / total_rows * 100, 2)
    else:
        duplicate_percentage = 0.0
    dataset_name = filename.replace("_validation_report.json", ".csv")

    return {
        "dataset": dataset_name,
        "total_rows": total_rows,
        "total_columns": report.get("total_columns", 0),
        "total_missing_values": total_missing,
        "duplicate_complete_rows": duplicate_rows,
        "duplicate_percentage": duplicate_percentage,
        "missing_required_columns": len(
            report.get("missing_required_columns", [])
        ),
    }

def main():
    summaries=[]
    missing_reports=[]
    
    for filename in REPORT_FILES:
        report_path=REPORTS_DIR/filename
        if not report_path.exists():
            missing_reports.append(filename)
            continue
        try:
            report=load_report(report_path)
            summaries.append(extract_quality_metrics(report,filename))
        except (json.JSONDecodeError, OSError) as error:
            print(f"Could not read {filename}: {error}")

    # Save consolidated JSON report
    output_json=REPORTS_DIR/"consolidated_quality_report.json"
    consolidated_report={
        "datasets_processed": len(summaries),
        "missing_report_files": missing_reports,
        "dataset_summaries": summaries,
    }

    with open(output_json, "w", encoding="utf-8") as file:
        json.dump(consolidated_report,file,indent=4)

    # Save a CSV summary for easy inspection
    output_csv=REPORTS_DIR/"consolidated_quality_summary.csv"

    if summaries:
        summary_df=pd.DataFrame(summaries)
        summary_df.to_csv(output_csv,index=False)

    print("\nCONSOLIDATED DATA QUALITY SUMMARY")
    print("=" * 55)
    print(f"Reports processed: {len(summaries)}")
    print(f"Reports missing: {len(missing_reports)}")

    for summary in summaries:
        print(
            f"{summary['dataset']}: "
            f"{summary['total_rows']} rows, "
            f"{summary['total_missing_values']} missing values, "
            f"{summary['duplicate_complete_rows']} duplicate rows"
        )

    if missing_reports:
        print("\nMissing reports:")
        for filename in missing_reports:
            print(f"- {filename}")

    print(f"\nJSON report: {output_json}")
    print(f"CSV summary: {output_csv}")

if __name__ == "__main__":
    main()