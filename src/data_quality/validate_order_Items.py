from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/olist_order_items_dataset.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_order_items(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Order_items dataset not found:{file_path}")
    return pd.read_csv(file_path)


def validate_orders(df:pd.DataFrame):
    required_columns=["order_id","order_item_id","product_id","seller_id","shipping_limit_date","price","freight_value"]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")

    missing_values={column:int(count) for column,count in df.isnull().sum().items()}
    duplicate_order_items=int(df.duplicated(subset=["order_id","order_item_id"]).sum())
    duplicate_rows=int(df.duplicated().sum())

    blank_identifiers={}
    for column in ['order_id','product_id','seller_id']:
        blank_identifiers[column]=int(df[column].astype("string").str.strip().eq("").sum())

    df['price']=pd.to_numeric(df["price"],errors="coerce")
    df['freight_value']=pd.to_numeric(df["freight_value"],errors="coerce")
    invalid_prices=int((df['price'].isna()|(df['price']<=0)).sum())
    invalid_freight_values=int((df['freight_value'].isna()|(df['freight_value']<0)).sum())

    shipping_dates=pd.to_datetime(df['shipping_limit_date'],errors="coerce")
    invalid_shipping_dates=int(shipping_dates.isna().sum())

    missing_order_ids=int(df['order_id'].isna().sum())
    missing_product_ids=int(df['product_id'].isna().sum())
    missing_seller_ids=int(df['seller_id'].isna().sum())

    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_values.items()
        },
        "duplicate_order_items": duplicate_order_items,
        "duplicate_full_rows": duplicate_rows,
        "blank_order_items_ids": blank_identifiers,
        "invalid_prices": invalid_prices,
        "invalid_freight_values": invalid_freight_values,
        "invalid_shipping_dates":invalid_shipping_dates,
        "missing_order_ids":missing_order_ids,
        "missing_product_ids":missing_product_ids,
        "missing_seller_ids":missing_seller_ids
    }
    return report

def main():
    order_items=load_order_items(DATA_FILE)
    report=validate_orders(order_items)
    report_path=REPORT_DIR/"order_items_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\nOrder_items Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()