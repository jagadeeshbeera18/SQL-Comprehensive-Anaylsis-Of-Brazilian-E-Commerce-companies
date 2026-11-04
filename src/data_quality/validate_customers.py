from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/olist_customers_dataset.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_orders(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Customers dataset not found:{file_path}")
    return pd.read_csv(file_path,dtype={"customer_zip_code_perfix":"string","customer_state":"string"})


def validate_customers(df:pd.DataFrame):
    required_columns=["customer_id","customer_unique_id","customer_zip_code_prefix","customer_city","customer_state"]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")

    missing_value_count=(df[required_columns].isna().sum().to_dict())
    duplicate_customer_id=int(df['customer_id'].duplicated().sum())
    duplicate_rows=int(df.duplicated().sum())
    blank_customer_ids=int(df['customer_id'].astype("string").str.strip().eq("").sum())
    state_codes = df["customer_state"].str.strip()
    valid_states = state_codes.str.fullmatch(r"^[A-Z]{2}$", na=False)
    invalid_state_codes = int((state_codes.notna() & ~valid_states).sum())
    zip_codes = df["customer_zip_code_prefix"].astype(str).str.strip()
    valid_zips = zip_codes.str.fullmatch(r"^\d{5}$", na=False)
    invalid_zip_codes = int((zip_codes.notna() & ~valid_zips).sum())

    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_value_count.items()
        },
        "duplicate_order_ids": duplicate_customer_id,
        "duplicate_full_rows": duplicate_rows,
        "blank_order_ids": blank_customer_ids,
        "invalid_state_codes": invalid_state_codes,
        "invalid_zip_codes": invalid_zip_codes
    }
    return report

  

def main():
    customers=load_orders(DATA_FILE)
    report=validate_customers(customers)
    report_path=REPORT_DIR/"customers_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\nCustomers Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()