from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/olist_orders_dataset.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_orders(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Orders dataset not found:{file_path}")
    return pd.read_csv(file_path)


def validate_orders(df:pd.DataFrame):
    required_columns=["order_id","customer_id","order_status","order_purchase_timestamp","order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        ]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")

    date_columns=["order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date",
        "order_estimated_delivery_date",]
    for column in date_columns:
        df[column]=pd.to_datetime(df[column],errors="coerce")

    missing_value_count=(df[required_columns].isna().sum().to_dict())
    duplicate_order_id=int(df['order_id'].duplicated().sum())
    duplicate_rows=int(df.duplicated().sum())
    blank_order_ids=int(df['order_id'].astype("string").str.strip().eq("").sum())
    delivered_before_purchase=int((df["order_delivered_customer_date"]<df["order_purchase_timestamp"]).sum())
    estimated_before_purchase=int((df["order_estimated_delivery_date"]<df["order_purchase_timestamp"]).sum())

    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_value_count.items()
        },
        "duplicate_order_ids": duplicate_order_id,
        "duplicate_full_rows": duplicate_rows,
        "blank_order_ids": blank_order_ids,
        "delivered_before_purchase": delivered_before_purchase,
        "estimated_delivery_before_purchase": estimated_before_purchase
    }
    return report

def main():
    orders=load_orders(DATA_FILE)
    report=validate_orders(orders)
    report_path=REPORT_DIR/"orders_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\nOrders Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()