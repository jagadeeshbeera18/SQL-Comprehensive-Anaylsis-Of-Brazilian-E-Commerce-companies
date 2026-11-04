from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/olist_order_payments_dataset.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_payment(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Order_Payments dataset not found:{file_path}")
    return pd.read_csv(file_path)


def validate_orders(df:pd.DataFrame):
    required_columns=["order_id","payment_sequential","payment_type","payment_installments","payment_value"]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")
    
    missing_values={column:int(count) for column,count in df.isnull().sum().items()}
    duplicate_payment_keys=int(df.duplicated(subset=["order_id","payment_sequential"]).sum())
    duplicate_rows=int(df.duplicated().sum())

    blank_payment_values={}
    for column in ["order_id","payment_type"]:
        blank_payment_values[column]=int(df[column].astype("string").str.strip().eq("").sum())

    df["payment_value"]=pd.to_numeric(df["payment_value"],errors='coerce')
    df["payment_installments"]=pd.to_numeric(df["payment_installments"],errors='coerce')
    df["payment_sequential"]=pd.to_numeric(df["payment_sequential"],errors='coerce')

    invalid_payment_values=int((df['payment_value'].isna()|(df["payment_value"]<0)).sum())
    invalid_payment_installments=int((df['payment_installments'].isna()|(df["payment_installments"]<1)|(df["payment_installments"]%1!=0)).sum())
    invalid_payment_sequence=int((df['payment_sequential'].isna()|(df["payment_sequential"]<1)|(df["payment_sequential"]%1!=0)).sum())

    payment_type_distribution={str(key):int(value) for key,value in df['payment_type'].fillna('missing').value_counts().items()}

    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_values.items()
        },
        "duplicate_payment_ids": duplicate_payment_keys,
        "duplicate_full_rows": duplicate_rows,
        "blank_payment_values": blank_payment_values,
        "invalid_payment_values": invalid_payment_values,
        "invalid_payment_installments": invalid_payment_installments,
        "invalid_payment_sequence": invalid_payment_sequence,
        "payment_type_dis":payment_type_distribution
    }
    return report

def main():
    payments=load_payment(DATA_FILE)
    report=validate_orders(payments)
    report_path=REPORT_DIR/"payments_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\npayments Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()