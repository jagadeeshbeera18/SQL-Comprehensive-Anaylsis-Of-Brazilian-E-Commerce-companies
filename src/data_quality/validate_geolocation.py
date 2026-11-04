from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/olist_geolocation_dataset.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_geolocation(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Geolocation dataset not found:{file_path}")
    return pd.read_csv(file_path)


def validate_geolocation(df:pd.DataFrame):
    required_columns=["geolocation_zip_code_prefix","geolocation_lat","geolocation_lng",
                      "geolocation_city","geolocation_state"]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")
    missing_values={column:int(count) for column,count in df.isnull().sum().items()}
    duplicate_rows=int(df.duplicated().sum())
    blank_identifiers={}
    for column in ["geolocation_city","geolocation_state"]:
        blank_identifiers[column]=int(df[column].astype("string").str.strip().eq("").sum())

    zip_codes=df['geolocation_zip_code_prefix'].astype(str).str.strip()
    invalid_zip_codes=int((zip_codes.isna()|~zip_codes.str.fullmatch(r'^\d{5}',na=False)).sum())
    coords=["geolocation_lat","geolocation_lng"]
    for col in coords:
        df[col]=pd.to_numeric(df[col], errors="coerce")

    invalid_lat=int((df['geolocation_lat'].isna()|~df['geolocation_lat'].between(-90,90)).sum())
    invalid_lng=int((df['geolocation_lng'].isna()|~df['geolocation_lng'].between(-180,180)).sum())

    state_distribution={str(key):int(value) for key,value in df['geolocation_state'].value_counts(dropna=False).items()}

    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_values.items()
        },
        "duplicate_full_rows": duplicate_rows,
        "blank_values": blank_identifiers,
        "invalid_zip_codes": invalid_zip_codes,
        "invalid_lat": invalid_lat,
        "invalid_lng": invalid_lng,
        "state_distribution":state_distribution
    }
    return report

def main():
    geolocation=load_geolocation(DATA_FILE)
    report=validate_geolocation(geolocation)
    report_path=REPORT_DIR/"order_geolocation_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\nOrder geolocation Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()