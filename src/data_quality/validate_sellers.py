from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/olist_sellers_dataset.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_sellers(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Sellers dataset not found:{file_path}")
    return pd.read_csv(file_path)


def validate_orders(df:pd.DataFrame):
    required_columns=["seller_id","seller_zip_code_prefix","seller_city","seller_state"]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")

    missing_value_count=(df[required_columns].isna().sum().to_dict())
    duplicate_seller_id=int(df['seller_id'].duplicated().sum())
    duplicate_rows=int(df.duplicated().sum())
    blank_values={}
    for column in ['seller_id',"seller_zip_code_prefix","seller_city","seller_state"]:
        blank_values[column]=int(df[column].astype("string").str.strip().eq("").sum())

    zip_code = df["seller_zip_code_prefix"].astype(str).str.strip()
    valid_zip_codes=zip_code.str.fullmatch(r'^\d{5}$',na=False)
    invalid_zip_codes=int((zip_code.isna() & ~valid_zip_codes).sum())

    states=df["seller_state"].astype(str).str.strip()
    vaild_states=states.str.fullmatch(r'^[A-Za-z]{2}$',na=False)
    invalid_states=int((states.isna()|~vaild_states).sum())

    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_value_count.items()
        },
        "duplicate_seller_ids": duplicate_seller_id,
        "duplicate_full_rows": duplicate_rows,
        "blank_seller_keys": blank_values,
        "invalid_zip_codes": invalid_zip_codes,
        "invalid_states": invalid_states
    }
    return report

def main():
    sellers=load_sellers(DATA_FILE)
    report=validate_orders(sellers)
    report_path=REPORT_DIR/"sellers_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\nSellers Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()